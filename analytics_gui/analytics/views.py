import base64
import itertools
import json
import os

import pdfkit
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone

from analytics_gui.analytics import utils
from analytics_gui.analytics.forms import CreateCaseForm, CreateAtmFormSet, AnalyticForm
from analytics_gui.analytics.models import Case, AtmJournal, AtmCase, AtmEventViewerEvent
from analytics_gui.analytics.parsers import parse_log_file, parse_window_event_viewer
from analytics_gui.companies.models import Company


@login_required(login_url='/login')
def create(request):
    company = Company.objects.get(users=request.user.dash_user)

    form = CreateCaseForm(company=company)
    atm_form_set = CreateAtmFormSet(company=company)

    if request.method == 'POST':
        form = CreateCaseForm(request.POST, request.FILES, company=company)
        if form.is_valid():
            case = form.save(commit=False)
            case.analyst = request.user.dash_user
            atm_form_set = CreateAtmFormSet(
                request.POST, request.FILES, instance=case, company=company)
            if atm_form_set.is_valid():
                case.save()
                atms = atm_form_set.save()
                for index, atm in enumerate(atms):
                    journal_virtual_key = 'atms-{}-journal_virtual[]'.format(index)
                    journal_files = request.FILES.getlist(journal_virtual_key)
                    if len(journal_files) > 0:
                        AtmJournal.objects.filter(atm=atm).delete()
                        [AtmJournal.objects.create(atm=atm, file=journal_file) for journal_file in
                         journal_files]

                if 'save' in request.POST:
                    return HttpResponseRedirect(reverse("base:dashboard"))
                elif 'analyze' in request.POST:
                    return HttpResponseRedirect(reverse("analytics:analyze", args=[case.id]))

    return render(request, 'analytics/create.html', {
        'form': form,
        'atm_form_set': atm_form_set,
        'company': company,
        'create': True,
    })


@login_required(login_url='/login')
def view_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    company = Company.objects.get(users=request.user.dash_user)
    form = CreateCaseForm(instance=case, company=company)
    atm_form_set = CreateAtmFormSet(instance=case, company=company)

    if request.method == 'POST':
        form = CreateCaseForm(request.POST, request.FILES, instance=case, company=company)
        atm_form_set = CreateAtmFormSet(
            request.POST, request.FILES, instance=case, company=company)
        if form.is_valid() and atm_form_set.is_valid():
            case.save()
            atm_form_set.save()
            for index, atm_form in enumerate(atm_form_set):
                if not atm_form.instance.id:
                    continue

                journal_virtual_key = 'atms-{}-journal_virtual[]'.format(index)
                journal_files = request.FILES.getlist(journal_virtual_key)
                if len(journal_files) > 0:
                    AtmJournal.objects.filter(atm=atm_form.instance).delete()
                    [AtmJournal.objects.create(atm=atm_form.instance, file=journal_file) for journal_file in
                     journal_files]

            if 'analyze' in request.POST:
                return HttpResponseRedirect(reverse("analytics:analyze", args=[case.id]))

    return render(request, 'analytics/create.html', {
        'form': form,
        'atm_form_set': atm_form_set,
        'company': company,
        'create': False,
    })


@login_required(login_url='/login')
def analyze_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    atms = case.atms.all()
    form = AnalyticForm(instance=case)

    journal_traces = []
    event_viewer_traces = []
    windows_events = {
        "are_there": False,
        "min_date": None,
        "max_date": None,
        "keys": []
    }
    meta = {
        "transactions_number": 0,
        "dates": {
            "min": None,
            "max": None,
        },
        "amount": {
            "valid_transactions": 0,
            "critical_errors_transactions": 0,
            "important_errors_transactions": 0,
        },
        "errors": {
            "critics_number": 0,
            "names": []
        }
    }

    for index, atm in enumerate(atms):
        # windows events
        if atm.microsoft_event_viewer:
            windows_events["are_there"] = True
            # get the min and max dates for filter
            if not windows_events["min_date"] \
                    or windows_events["min_date"] > atm.event_viewer_errors.first().event_date:
                windows_events["min_date"] = atm.event_viewer_errors.first().event_date
            if not windows_events["max_date"] \
                    or windows_events["max_date"] < atm.event_viewer_errors.last().event_date:
                windows_events["max_date"] = atm.event_viewer_errors.last().event_date
            # get the keys of records id
            event_id_keys = set(atm.event_viewer_errors.values_list('event_id', flat=True).distinct())
            in_all_events_keys = set(windows_events["keys"])
            in_record_id_keys_but_not_in_all = event_id_keys - in_all_events_keys
            windows_events["keys"] = windows_events["keys"] + list(in_record_id_keys_but_not_in_all)

        # Journals Virtual
        for journal_file in atm.journals.all():
            trace, meta_journal = parse_log_file(journal_file.file.file, index)
            journal_traces.append(trace)
            # save only new errors names
            in_all_errors_names = set(meta["errors"]["names"])
            in_errors_names_but_not_in_all = meta_journal["errors"]["names"] - in_all_errors_names
            meta["errors"]["names"] = meta["errors"]["names"] + list(in_errors_names_but_not_in_all)
            # save meta
            meta["transactions_number"] += meta_journal["transactions_number"]
            meta["amount"]["valid_transactions"] += meta_journal["amount"]["valid_transactions"]
            meta["amount"]["critical_errors_transactions"] += meta_journal["amount"]["critical_errors_transactions"]
            meta["amount"]["important_errors_transactions"] += meta_journal["amount"]["important_errors_transactions"]
            meta["errors"]["critics_number"] += meta_journal["errors"]["critics_number"]
            if not meta["dates"]["min"] or meta["dates"]["min"] > meta_journal["dates"]["min"]:
                meta["dates"]["min"] = meta_journal["dates"]["min"]
            if not meta["dates"]["max"] or meta["dates"]["max"] < meta_journal["dates"]["max"]:
                meta["dates"]["max"] = meta_journal["dates"]["max"]

    if request.method == 'POST':
        form = AnalyticForm(request.POST, instance=case)
        if form.is_valid():
            case = form.save(commit=False)
            if 'close-status' in request.POST:
                case.status = Case.STATUS_CLOSE
                case.save()
            if 'open-status' in request.POST:
                case.status = Case.STATUS_OPEN
                case.save()

        if 'event_start_date_timeline' in request.POST and 'event_end_date_timeline' in request.POST:
            start_date = request.POST['event_start_date_timeline']
            end_date = request.POST['event_end_date_timeline']
            events = AtmEventViewerEvent.objects.filter(event_date__range=(start_date, end_date))
            events_response = []
            for event in events:
                events_response.append({
                    "date": event.event_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "eventId": event.event_id,
                    "eventRecordId": event.event_record_id,
                    "context": event.context,
                    "className": "window-event",
                    "color": settings.COLOR_BLUE
                })
            return JsonResponse(events_response, safe=False, status=200)

    journal_traces = list(itertools.chain(*journal_traces))

    meta["errors"]["critics_number_percentage"] = meta["errors"]["critics_number"] * 100 / meta["transactions_number"]
    # get the currency
    currency = case.get_missing_amount_currency_display()
    currency = currency[currency.index("-") + 1:currency.index("|")].strip()

    # serialize the min and max dates
    if windows_events["min_date"] is not None and windows_events["max_date"] is not None:
        windows_events["min_date"] = windows_events["min_date"].strftime("%Y-%m-%d %H:%M:%S")
        windows_events["max_date"] = windows_events["max_date"].strftime("%Y-%m-%d %H:%M:%S")
    if meta["dates"]["min"] is not None and meta["dates"]["max"] is not None:
        meta["dates"]["min"] = meta["dates"]["min"].strftime("%Y-%m-%d %H:%M:%S")
        meta["dates"]["max"] = meta["dates"]["max"].strftime("%Y-%m-%d %H:%M:%S")

    return render(request, 'analytics/results.html', {
        'case': case,
        'form': form,
        'journal_traces': journal_traces,
        'event_viewer_traces': event_viewer_traces,
        'meta': meta,
        'windows_events': windows_events,
        'currency': currency,
        'COLOR_GREEN': settings.COLOR_GREEN,
        'COLOR_RED': settings.COLOR_RED,
        'COLOR_ORANGE': settings.COLOR_ORANGE,
        'COLOR_BLUE': settings.COLOR_BLUE,
    })


def delete_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    case.delete()
    return HttpResponseRedirect(reverse("base:dashboard"))


def generate_pdf(request, case_id):
    args = None
    case = get_object_or_404(Case, id=case_id)
    atms = case.atms.all()
    images = dict()
    files = []
    case_picture = None
    company_logo = None
    atm_locations = []
    options = {
        'margin-bottom': '0.75in',
        'footer-right': '[page]'
    }

    if case.picture:
        case_picture = settings.BASE_DIR + case.picture.url
    elif case.bank.company.logo:
        company_logo = settings.BASE_DIR + case.bank.company.logo.url

    bootstrap = os.path.join(settings.BASE_DIR, 'base', 'static', 'css', 'bootstrap.min.css')
    base = os.path.join(settings.BASE_DIR, 'base', 'static', 'css', 'base.css')
    image_root = os.path.join(settings.BASE_DIR, 'media/')
    logo = os.path.join(settings.BASE_DIR, 'base', 'static', 'images', 'cyttek-group.png')
    default_avatar = os.path.join(settings.BASE_DIR, 'base', 'static', 'images', 'default_avatar.png')
    html_template = 'analytics/pdf_template.html'

    meta = {
        "transactions_number": 0,
        "amount": {
            "valid_transactions": 0,
            "critical_errors_transactions": 0,
            "important_errors_transactions": 0,
        },
        "errors": {
            "critics_number": 0,
            "names": []
        }
    }

    for index, atm in enumerate(atms):
        tmp = {}
        for loc in atm.atm_location.all():
            atm_locations.append(loc.address)
        # Microsoft Event Viewer
        if atm.microsoft_event_viewer:
            files.append(utils.create_file_element(atm.microsoft_event_viewer.name))

        # Other log
        if atm.other_log:
            files.append(utils.create_file_element(atm.other_log.name))

        # Cash replacement schedule
        if atm.cash_replacement_schedule:
            files.append(utils.create_file_element(atm.cash_replacement_schedule.name))

        # Journals Virtual
        for journal_file in atm.journals.all():
            tmp = {}
            trace, meta_journal = parse_log_file(journal_file.file.file, index)

            files.append(utils.create_file_element(journal_file.file.name))

            # save only new errors names
            in_all_errors_names = set(meta["errors"]["names"])
            in_errors_names_but_not_in_all = meta_journal["errors"]["names"] - in_all_errors_names
            meta["errors"]["names"] = meta["errors"]["names"] + list(in_errors_names_but_not_in_all)
            # save meta
            meta["transactions_number"] += meta_journal["transactions_number"]
            meta["amount"]["valid_transactions"] += meta_journal["amount"]["valid_transactions"]
            meta["amount"]["critical_errors_transactions"] += meta_journal["amount"]["critical_errors_transactions"]
            meta["amount"]["important_errors_transactions"] += meta_journal["amount"]["important_errors_transactions"]
            meta["errors"]["critics_number"] += meta_journal["errors"]["critics_number"]

    meta["errors"]["critics_number_percentage"] = meta["errors"]["critics_number"] * 100 / meta["transactions_number"]
    currency = case.get_missing_amount_currency_display()
    currency = currency[currency.index("-") + 1:currency.index("|")].strip()

    if request.is_ajax():
        args = dict(request.POST.iterlists())
        for key in args.keys():
            if 'chart' in key:
                image_data = base64.b64decode(args[key][0])
                if 'timeline' in key:
                    filename = key + ".png"
                else:
                    filename = key + ".svg"
                with open(image_root + filename, 'w') as f:
                    f.write(image_data)
                    images[key.replace('-', '_')] = image_root + filename

    time_line_table = utils.build_table(
        args['time_line[Fecha][]'],
        args['time_line[Error][]'],
        args['time_line[Monto][]']
    )

    operations_table = utils.build_table(
        args['operations[Fecha][]'],
        args['operations[Error][]'],
        args['operations[Monto][]']
    )

    args.update(images)
    args['case'] = case
    args['date'] = timezone.now()
    args['logo'] = logo
    args['time_line_table'] = time_line_table
    args['operations_table'] = operations_table
    args['currency'] = currency
    args['meta'] = meta
    args['atm_locations'] = atm_locations
    args['case_picture'] = case_picture
    args['company_logo'] = company_logo
    args['default_avatar'] = default_avatar
    args['files'] = files
    args['analyst_name'] = \
        request.user.first_name + \
        " " + \
        request.user.last_name if request.user.first_name != '' else request.user.username

    rendered_html = render_to_string(html_template, args)

    style_list = [bootstrap, base]

    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'footer-center': '[page]',
        'footer-font-size': '12'
        # 'header-left': 'LOGO'
    }

    pdfkit.from_string(rendered_html, image_root + 'report.pdf', css=style_list, options=options)

    for image in images.values():
        os.remove(image)

    with open(image_root + 'report.pdf', 'rb') as pdf_file:
        return HttpResponse(
            json.dumps({'file': base64.b64encode(pdf_file.read())}),
            content_type="application/pdf")


@receiver(post_save, sender=AtmCase)
def parse_window_event_errors(sender, **kwargs):
    if kwargs['instance'].microsoft_event_viewer:
        parse_window_event_viewer(kwargs['instance'])
