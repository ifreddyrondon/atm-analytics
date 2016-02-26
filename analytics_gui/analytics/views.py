import itertools

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from analytics_gui.analytics.forms import CreateCaseForm, CreateAtmFormSet, AnalyticForm
from analytics_gui.analytics.models import Case, AtmJournal
from analytics_gui.analytics.parsers import parse_log_file
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
        # Microsoft Event Viewer
        # if atm.microsoft_event_viewer:
        #     event_viewer_traces = parse_window_event_viewer(atm.microsoft_event_viewer.file)
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

    journal_traces = list(itertools.chain(*journal_traces))

    meta["errors"]["critics_number_percentage"] = meta["errors"]["critics_number"] * 100 / meta["transactions_number"]
    currency = case.get_missing_amount_currency_display()
    currency = currency[currency.index("-") + 1:currency.index("|")].strip()

    return render(request, 'analytics/results.html', {
        'case': case,
        'form': form,
        'journal_traces': journal_traces,
        'event_viewer_traces': event_viewer_traces,
        'meta': meta,
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
