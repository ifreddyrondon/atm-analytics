import csv

import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from analytics_gui.companies.forms import ConfigForm, BankFormSet, CompanyAtmLocationFormSet
from analytics_gui.companies.models import Company, CompanyAtmLocation, Bank, AtmRepositionEvent


@login_required(login_url='/login')
def config(request):
    user = request.user.dash_user
    company = Company.objects.get(users=user)

    config_form = ConfigForm(instance=company)
    bank_form_set = BankFormSet(instance=company)
    atm_location_form_set = CompanyAtmLocationFormSet(instance=company)

    if request.method == 'POST':
        config_form = ConfigForm(request.POST, request.FILES, instance=company)
        bank_form_set = BankFormSet(request.POST, instance=company)
        atm_location_form_set = CompanyAtmLocationFormSet(request.POST, instance=company)
        if config_form.is_valid() and bank_form_set.is_valid() and atm_location_form_set:
            config_form.save()
            bank_form_set.save()
            atm_location_form_set.save()

            if 'address_csv' in request.FILES:
                reader = csv.reader(request.FILES["address_csv"])
                for row in reader:
                    CompanyAtmLocation.objects.get_or_create(address=row[0], company=company)

            if 'atms_reposition_events' in request.FILES:
                reader = csv.reader(request.FILES["atms_reposition_events"])
                for row in reader:
                    try:
                        bank = Bank.objects.get(company=company, name=row[0])
                        atm_direction = CompanyAtmLocation.objects.get(company=company, address=row[1])
                        reposition_event_data = datetime.datetime.strptime(row[2], "%d/%m/%Y %H:%M")
                        AtmRepositionEvent.objects.get_or_create(bank=bank, location=atm_direction,
                                                                 reposition_date=reposition_event_data)
                    except (Bank.DoesNotExist, CompanyAtmLocation.DoesNotExist):
                        continue

            return HttpResponseRedirect(reverse("companies:config"))

    return render(request, 'companies/config.html', {
        "company": company,
        "form": config_form,
        "bank_form_set": bank_form_set,
        "atm_location_form_set": atm_location_form_set,
    })
