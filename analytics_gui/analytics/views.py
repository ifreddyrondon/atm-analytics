import base64
import json
import os

import pdfkit
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone

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

    # from pprint import pprint

    for atm in atms:
        for journal_file in atm.journals.all():
            trace = parse_log_file(journal_file.file.file)
            # pprint(trace)

    if request.method == 'POST':
        form = AnalyticForm(request.POST, instance=case)
        if form.is_valid():
            case = form.save(commit=False)
            if 'close' in request.POST:
                case.status = Case.STATUS_CLOSE
            case.save()

    return render(request, 'analytics/results.html', {
        'case': case,
        'atms': atms,
        'form': form,
    })


def delete_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    case.delete()
    return HttpResponseRedirect(reverse("base:dashboard"))


def generate_pdf(request, case_id):
    args = None

    bootstrap = os.path.join(settings.BASE_DIR, 'base', 'static', 'css', 'bootstrap.min.css')
    base = os.path.join(settings.BASE_DIR, 'base', 'static', 'css', 'base.css')
    image_root = os.path.join(settings.BASE_DIR, 'base', 'static', 'images/')

    html_template = 'analytics/pdf_template.html'

    images = dict()
    if request.is_ajax():
        args = dict(request.POST.iterlists())
        for key in args.keys():
            if 'chart' in key:
                image_data = base64.b64decode(args[key][0])
                filename = key + ".svg"
                with open(image_root + filename, 'w') as f:
                    f.write(image_data)
                    images[key.replace('-', '_')] = image_root + filename

    case = get_object_or_404(Case, id=case_id)

    args.update(images)
    args['case'] = case
    args['date'] = timezone.now()

    rendered_html = render_to_string(html_template, args)

    style_list = [bootstrap, base]

    try:
        pdfkit.from_string(rendered_html, 'report.pdf', css=style_list)
    except Exception as e:
        if "code 1" in e:
            pass

    for image in images.values():
        os.remove(image)

    with open('report.pdf', 'rb') as pdf_file:
        return HttpResponse(
            json.dumps({'file': base64.b64encode(pdf_file.read())}),
            content_type="application/pdf")
