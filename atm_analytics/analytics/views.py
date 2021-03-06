import base64
import datetime
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

from atm_analytics.analytics import utils
from atm_analytics.analytics.decorators import format_for_xfs_files_required, select_xfs_format_required
from atm_analytics.analytics.forms import CreateCaseForm, CreateAtmFormSet, AnalyticForm
from atm_analytics.analytics.models import Case, AtmJournal, AtmCase, AtmEventViewerEvent
from atm_analytics.analytics.parsers import parse_log_file, parse_window_event_viewer
from atm_analytics.companies.models import Company, AtmRepositionEvent, XFSFormat


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
@format_for_xfs_files_required()
@select_xfs_format_required()
def analyze_case(request, case_id, atms_with_format=None):
    # threshold to find close events, 5 min
    threshold_time = 300
    case = get_object_or_404(Case, id=case_id)
    company = case.bank.company
    atms = case.atms.all()
    form = AnalyticForm(instance=case)

    if atms_with_format:
        atms_id_with_format = [int(item[0]) for item in json.loads(atms_with_format)]
        formats_id = [int(item[1]) for item in json.loads(atms_with_format)]

    traces = {
        "journal": [],
        "reposition": [],
    }

    meta = {
        "journal": {
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
        },
        "windows": {
            "are_there": False,
            "min_date": None,
            "max_date": None,
            "keys": [],
            "count": 0,
        },
        "reposition": {
            "min_date": None,
            "max_date": None,
            "count": 0,
            "atms_count": [],
            "close_events_count": 0,
        }
    }

    for index, atm in enumerate(atms):
        # windows events
        if atm.microsoft_event_viewer:
            meta["windows"]["are_there"] = True
            # get the min and max dates for filter
            if not meta["windows"]["min_date"] \
                    or meta["windows"]["min_date"] > atm.event_viewer_errors.first().event_date:
                meta["windows"]["min_date"] = atm.event_viewer_errors.first().event_date
            if not meta["windows"]["max_date"] \
                    or meta["windows"]["max_date"] < atm.event_viewer_errors.last().event_date:
                meta["windows"]["max_date"] = atm.event_viewer_errors.last().event_date
            # get the keys of records id
            event_id_keys = set(atm.event_viewer_errors.values_list('event_id', flat=True).distinct())
            in_all_events_keys = set(meta["windows"]["keys"])
            in_record_id_keys_but_not_in_all = event_id_keys - in_all_events_keys
            meta["windows"]["keys"] = meta["windows"]["keys"] + list(in_record_id_keys_but_not_in_all)
            meta["windows"]["count"] += atm.event_viewer_errors.count()

        # Journals Virtual
        meta_journal = None
        for journal_file in atm.journals.all():
            # get XFSFormat or continue
            xfs_format = None
            if atms_with_format and atm.id in atms_id_with_format:
                # get index id on list
                index = atms_id_with_format.index(atm.id)
                xfs_format = XFSFormat.objects.get(id=formats_id[index])
            else:
                xfs_format = XFSFormat.objects.filter(
                    company=company, hardware=atm.hardware, software=atm.software)
                if len(xfs_format) > 0:
                    xfs_format = xfs_format[0]

            if not xfs_format:
                continue

            trace, meta_journal = parse_log_file(journal_file.file.file, index, xfs_format)
            traces["journal"].append(trace)
            # save only new errors names
            in_all_errors_names = set(meta["journal"]["errors"]["names"])
            in_errors_names_but_not_in_all = meta_journal["errors"]["names"] - in_all_errors_names
            meta["journal"]["errors"]["names"] = meta["journal"]["errors"]["names"] + list(
                in_errors_names_but_not_in_all)
            # save meta
            meta["journal"]["transactions_number"] += meta_journal["transactions_number"]
            meta["journal"]["amount"]["valid_transactions"] += meta_journal["amount"]["valid_transactions"]
            meta["journal"]["amount"]["critical_errors_transactions"] += meta_journal["amount"][
                "critical_errors_transactions"]
            meta["journal"]["amount"]["important_errors_transactions"] += meta_journal["amount"][
                "important_errors_transactions"]
            meta["journal"]["errors"]["critics_number"] += meta_journal["errors"]["critics_number"]
            if meta_journal["dates"]["min"] and (
                not meta["journal"]["dates"]["min"] or meta["journal"]["dates"]["min"] > meta_journal["dates"]["min"]):
                meta["journal"]["dates"]["min"] = meta_journal["dates"]["min"]
            if meta_journal["dates"]["max"] and (
                not meta["journal"]["dates"]["max"] or meta["journal"]["dates"]["max"] < meta_journal["dates"]["max"]):
                meta["journal"]["dates"]["max"] = meta_journal["dates"]["max"]

        if not meta_journal:
            continue

        # reposition events
        atm_reposition_events = AtmRepositionEvent.objects.filter(bank=case.bank, location=atm.atm_location.first())
        if len(atm_reposition_events) == 0:
            continue

        meta["reposition"]["atms_count"].append({
            'address': atm.atm_location.first().address,
            'count': len(atm_reposition_events),
            'date': atm_reposition_events[0].reposition_date.strftime("%H:%M")
        })

        meta["reposition"]["count"] += len(atm_reposition_events)
        for event in atm_reposition_events:
            # get the min and max dates for filter
            if not meta["reposition"]["min_date"] \
                    or meta["reposition"]["min_date"] > event.reposition_date:
                meta["reposition"]["min_date"] = event.reposition_date
            if not meta["reposition"]["max_date"] \
                    or meta["reposition"]["max_date"] < event.reposition_date:
                meta["reposition"]["max_date"] = event.reposition_date

            traces["reposition"].append({
                "date": event.reposition_date.strftime("%Y-%m-%d %H:%M:%S"),
                "address": event.location.address,
            })

            # find close windows events to this reposition event
            start_date = event.reposition_date - datetime.timedelta(seconds=threshold_time)
            end_date = event.reposition_date + datetime.timedelta(seconds=threshold_time)
            meta["reposition"]["close_events_count"] += AtmEventViewerEvent.objects.filter(
                atm__in=atms,
                event_date__range=(start_date, end_date)).count()

            # find close xfs events to this reposition event
            start_date = start_date.replace(tzinfo=None)
            end_date = end_date.replace(tzinfo=None)
            for xfs_date in meta_journal["dates"]["all"]:
                if start_date <= xfs_date <= end_date:
                    meta["reposition"]["close_events_count"] += 1

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
            events_response = []
            for atm in atms:
                events = AtmEventViewerEvent.objects.filter(atm=atm, event_date__range=(start_date, end_date))
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

    traces["journal"] = list(itertools.chain(*traces["journal"]))

    meta["journal"]["errors"]["critics_number_percentage"] = meta["journal"]["errors"]["critics_number"] * 100 / \
                                                             meta["journal"]["transactions_number"]

    # serialize the min and max dates
    if meta["windows"]["min_date"] is not None and meta["windows"]["max_date"] is not None:
        meta["windows"]["min_date"] = meta["windows"]["min_date"].strftime("%Y-%m-%d %H:%M:%S")
        meta["windows"]["max_date"] = meta["windows"]["max_date"].strftime("%Y-%m-%d %H:%M:%S")
    if meta["journal"]["dates"]["min"] is not None and meta["journal"]["dates"]["max"] is not None:
        meta["journal"]["dates"]["min"] = meta["journal"]["dates"]["min"].strftime("%Y-%m-%d %H:%M:%S")
        meta["journal"]["dates"]["max"] = meta["journal"]["dates"]["max"].strftime("%Y-%m-%d %H:%M:%S")
    if meta["reposition"]["min_date"] is not None and meta["reposition"]["max_date"] is not None:
        meta["reposition"]["min_date"] = meta["reposition"]["min_date"].strftime("%Y-%m-%d %H:%M:%S")
        meta["reposition"]["max_date"] = meta["reposition"]["max_date"].strftime("%Y-%m-%d %H:%M:%S")

    return render(request, 'analytics/results.html', {
        'case': case,
        'form': form,
        'traces': traces,
        'meta': meta,
        'COLORS': {
            'GREEN': settings.COLOR_GREEN,
            'RED': settings.COLOR_RED,
            'ORANGE': settings.COLOR_ORANGE,
            'BLUE': settings.COLOR_BLUE,
            'YELLOW': settings.COLOR_YELLOW,
        }
    })


def delete_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    case.delete()
    return HttpResponseRedirect(reverse("base:dashboard"))


@login_required(login_url='/login')
def no_format_available(request):
    return render(request, 'analytics/no_format_available_2_analyze.html', {})


@login_required(login_url='/login')
def select_xfs_format(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    company = case.bank.company
    atms = case.atms.all()
    atms_need_select_format = []
    atms_with_format = []

    for atm in atms:
        formats = XFSFormat.objects.filter(company=company, hardware=atm.hardware, software=atm.software)

        if len(formats) > 1:
            atms_need_select_format.append({
                'atm': atm,
                'formats': formats
            })

    if request.method == 'POST':
        atms_id = [k[6:] for k in request.POST.keys() if 'radio' in k]
        for atm_id in atms_id:
            format_id = request.POST['radio_' + atm_id]
            atms_with_format.append([atm_id, format_id])
        return HttpResponseRedirect(
            reverse("analytics:analyze-with-format", args=[case.id, json.dumps(atms_with_format)]))

    return render(request, 'analytics/select_xfs_format.html', {
        'atms_need_select_format': atms_need_select_format,
        'COLORS': {
            'GREEN': settings.COLOR_GREEN,
            'RED': settings.COLOR_RED,
            'ORANGE': settings.COLOR_ORANGE,
        }
    })


def generate_pdf(request, case_id):
    threshold_time = 300
    args = None
    case = get_object_or_404(Case, id=case_id)
    atms = case.atms.all()
    images = dict()
    files = []
    case_picture = None
    company_logo = None
    atm_locations = []

    traces = {
        "journal": [],
        "reposition": [],
    }

    if case.picture:
        case_picture = settings.BASE_DIR + case.picture.url
    elif case.bank.company.logo:
        company_logo = settings.BASE_DIR + case.bank.company.logo.url

    bootstrap = os.path.join(settings.BASE_DIR, 'base', 'static', 'css', 'bootstrap.min.css')
    base = os.path.join(settings.BASE_DIR, 'base', 'static', 'css', 'base.css')
    media_root = os.path.join(settings.BASE_DIR, 'media/')
    default_avatar = os.path.join(settings.BASE_DIR, 'base', 'static', 'images', 'default_avatar.png')
    html_template = 'analytics/pdf_template.html'

    meta = {
        "journal": {
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
        },
        "windows": {
            "are_there": False,
            "min_date": None,
            "max_date": None,
            "keys": [],
            "count": 0,
        },
        "reposition": {
            "min_date": None,
            "max_date": None,
            "count": 0,
            "atms_count": [],
            "close_events_count": 0,
        }
    }

    for index, atm in enumerate(atms):
        tmp = {}

        for loc in atm.atm_location.all():
            atm_locations.append(loc.address)

        # Other log
        if atm.other_log:
            files.append(utils.create_file_element(atm.other_log.name))

        # windows events
        if atm.microsoft_event_viewer:
            files.append(utils.create_file_element(atm.microsoft_event_viewer.name))
            meta["windows"]["are_there"] = True
            # get the min and max dates for filter
            if not meta["windows"]["min_date"] \
                    or meta["windows"]["min_date"] > atm.event_viewer_errors.first().event_date:
                meta["windows"]["min_date"] = atm.event_viewer_errors.first().event_date
            if not meta["windows"]["max_date"] \
                    or meta["windows"]["max_date"] < atm.event_viewer_errors.last().event_date:
                meta["windows"]["max_date"] = atm.event_viewer_errors.last().event_date
            # get the keys of records id
            event_id_keys = set(atm.event_viewer_errors.values_list('event_id', flat=True).distinct())
            in_all_events_keys = set(meta["windows"]["keys"])
            in_record_id_keys_but_not_in_all = event_id_keys - in_all_events_keys
            meta["windows"]["keys"] = meta["windows"]["keys"] + list(in_record_id_keys_but_not_in_all)
            meta["windows"]["count"] += atm.event_viewer_errors.count()

        # Journals Virtual
        for journal_file in atm.journals.all():
            trace, meta_journal = parse_log_file(journal_file.file.file, index)
            files.append(utils.create_file_element(journal_file.file.name))
            traces["journal"].append(trace)
            # save only new errors names
            in_all_errors_names = set(meta["journal"]["errors"]["names"])
            in_errors_names_but_not_in_all = meta_journal["errors"]["names"] - in_all_errors_names
            meta["journal"]["errors"]["names"] = meta["journal"]["errors"]["names"] + list(
                in_errors_names_but_not_in_all)
            # save meta
            meta["journal"]["transactions_number"] += meta_journal["transactions_number"]
            meta["journal"]["amount"]["valid_transactions"] += meta_journal["amount"]["valid_transactions"]
            meta["journal"]["amount"]["critical_errors_transactions"] += meta_journal["amount"][
                "critical_errors_transactions"]
            meta["journal"]["amount"]["important_errors_transactions"] += meta_journal["amount"][
                "important_errors_transactions"]
            meta["journal"]["errors"]["critics_number"] += meta_journal["errors"]["critics_number"]
            if not meta["journal"]["dates"]["min"] or meta["journal"]["dates"]["min"] > meta_journal["dates"]["min"]:
                meta["journal"]["dates"]["min"] = meta_journal["dates"]["min"]
            if not meta["journal"]["dates"]["max"] or meta["journal"]["dates"]["max"] < meta_journal["dates"]["max"]:
                meta["journal"]["dates"]["max"] = meta_journal["dates"]["max"]

        # reposition events
        atm_reposition_events = AtmRepositionEvent.objects.filter(bank=case.bank, location=atm.atm_location.first())
        meta["reposition"]["atms_count"].append({
            'address': atm.atm_location.first().address,
            'count': len(atm_reposition_events),
            'date': atm_reposition_events[0].reposition_date.strftime("%H:%M")
        })
        meta["reposition"]["count"] += len(atm_reposition_events)
        for event in atm_reposition_events:
            # get the min and max dates for filter
            if not meta["reposition"]["min_date"] \
                    or meta["reposition"]["min_date"] > event.reposition_date:
                meta["reposition"]["min_date"] = event.reposition_date
            if not meta["reposition"]["max_date"] \
                    or meta["reposition"]["max_date"] < event.reposition_date:
                meta["reposition"]["max_date"] = event.reposition_date

            traces["reposition"].append({
                "date": event.reposition_date.strftime("%Y-%m-%d %H:%M:%S"),
                "address": event.location.address,
            })

            # find close windows events to this reposition event
            start_date = event.reposition_date - datetime.timedelta(seconds=threshold_time)
            end_date = event.reposition_date + datetime.timedelta(seconds=threshold_time)
            meta["reposition"]["close_events_count"] += AtmEventViewerEvent.objects.filter(
                atm__in=atms,
                event_date__range=(start_date, end_date)).count()

            # find close xfs events to this reposition event
            start_date = start_date.replace(tzinfo=None)
            end_date = end_date.replace(tzinfo=None)
            for xfs_date in meta_journal["dates"]["all"]:
                if start_date <= xfs_date <= end_date:
                    meta["reposition"]["close_events_count"] += 1

    traces["journal"] = list(itertools.chain(*traces["journal"]))

    meta["journal"]["errors"]["critics_number_percentage"] = meta["journal"]["errors"]["critics_number"] * 100 / \
                                                             meta["journal"]["transactions_number"]

    # serialize the min and max dates
    if meta["windows"]["min_date"] is not None and meta["windows"]["max_date"] is not None:
        meta["windows"]["min_date"] = meta["windows"]["min_date"].strftime("%Y-%m-%d %H:%M:%S")
        meta["windows"]["max_date"] = meta["windows"]["max_date"].strftime("%Y-%m-%d %H:%M:%S")
    if meta["journal"]["dates"]["min"] is not None and meta["journal"]["dates"]["max"] is not None:
        meta["journal"]["dates"]["min"] = meta["journal"]["dates"]["min"].strftime("%Y-%m-%d %H:%M:%S")
        meta["journal"]["dates"]["max"] = meta["journal"]["dates"]["max"].strftime("%Y-%m-%d %H:%M:%S")
    if meta["reposition"]["min_date"] is not None and meta["reposition"]["max_date"] is not None:
        meta["reposition"]["min_date"] = meta["reposition"]["min_date"].strftime("%Y-%m-%d %H:%M:%S")
        meta["reposition"]["max_date"] = meta["reposition"]["max_date"].strftime("%Y-%m-%d %H:%M:%S")

    if request.is_ajax():
        args = dict(request.POST.iterlists())
        for key in args.keys():
            if 'chart' in key:
                if 'image/png' in args[key][0]:
                    image_data = base64.b64decode(args[key][0].split(",")[1])
                    filename = key + ".png"
                else:
                    image_data = base64.b64decode(args[key][0].split(",")[1])
                    filename = key + ".svg"
                with open(media_root + filename, 'w') as f:
                    f.write(image_data)
                    images[key] = media_root + filename

    time_line_table = utils.build_table(
        args['time_line[Fecha][]'],
        args['time_line[Error][]'],
        args['time_line[Monto][]'],
        args['time_line[ATM][]'],
        atms
    )

    operations_table = utils.build_table(
        args['operations[Fecha][]'],
        args['operations[Error][]'],
        args['operations[Monto][]'],
        args['operations[ATM][]'],
        atms
    )

    args.update(images)
    args['case'] = case
    args['date'] = timezone.now()
    args['time_line_table'] = time_line_table
    args['operations_table'] = operations_table
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
        'margin-right': '0.6in',
        'margin-bottom': '0.75in',
        'margin-left': '0.6in',
        'encoding': "UTF-8",
        'footer-center': '[page]',
        'footer-font-size': '10'
    }

    pdfkit.from_string(rendered_html, media_root + 'tmp_report.pdf', css=style_list, options=options)

    for image in images.values():
        os.remove(image)

    timeline_height = int(args['timeline_height'][0])
    operations_height = int(args['operations_height'][0])

    utils.add_header_and_rotate_timeline(media_root + 'tmp_report.pdf', timeline_height, operations_height)

    with open(media_root + 'report.pdf', 'rb') as pdf_file:
        return HttpResponse(
            json.dumps({'file': base64.b64encode(pdf_file.read())}),
            content_type="application/pdf")


@receiver(post_save, sender=AtmCase)
def parse_window_event_errors(sender, **kwargs):
    if kwargs['instance'].microsoft_event_viewer:
        parse_window_event_viewer(kwargs['instance'])
