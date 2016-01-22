from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from analytics_gui.analytics.forms import CreateCaseForm, CreateAtmFormSet
from analytics_gui.analytics.models import Case, AtmCase, AtmJournal


def dashboard(request):
    cases = Case.objects.all().order_by('number')

    return render(request, 'analytics/dashboard.html', {
        "cases": cases
    })


def create(request):
    form = CreateCaseForm()
    atm_form_set = CreateAtmFormSet()

    if request.method == 'POST':
        form = CreateCaseForm(data=request.POST)
        if form.is_valid():
            case = form.save(commit=False)

            atm_form_set = CreateAtmFormSet(request.POST, request.FILES, instance=case)
            if atm_form_set.is_valid():
                case.save()
                atms = atm_form_set.save()
                for index, atm in enumerate(atms):
                    journal_virtual_key = 'atms-{}-journal_virtual'.format(index)
                    journal_files = request.FILES.getlist(journal_virtual_key)
                    if journal_files > 0:
                        AtmJournal.objects.filter(atm=atm).delete()
                        for journal_file in request.FILES.getlist(journal_virtual_key):
                            AtmJournal.objects.create(atm=atm, file=journal_file)

                return HttpResponseRedirect(reverse("analytics:dashboard"))

    return render(request, 'analytics/create.html', {
        'form': form,
        'atm_form_set': atm_form_set,
        'create': True
    })


def view_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    form = CreateCaseForm(instance=case)
    atm_form_set = CreateAtmFormSet(instance=case)

    if request.method == 'POST':
        form = CreateCaseForm(data=request.POST, instance=case)
        atm_form_set = CreateAtmFormSet(request.POST, request.FILES, instance=case)
        if form.is_valid() and atm_form_set.is_valid():
            case.save()
            atm_form_set.save()
            for index, atm in enumerate(case.atms.all()):
                print(index)
                journal_virtual_key = 'atms-{}-journal_virtual'.format(index)
                journal_files = request.FILES.getlist(journal_virtual_key)
                if journal_files > 0:
                    AtmJournal.objects.filter(atm=atm).delete()
                    for journal_file in request.FILES.getlist(journal_virtual_key):
                        AtmJournal.objects.create(atm=atm, file=journal_file)

    return render(request, 'analytics/create.html', {
        'form': form,
        'atm_form_set': atm_form_set,
        'create': False
    })


def delete_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    case.delete()
    return HttpResponseRedirect(reverse("analytics:dashboard"))
