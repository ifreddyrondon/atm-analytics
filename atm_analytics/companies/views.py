import csv
import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from atm_analytics.analytics.utils import try_unicode
from atm_analytics.companies.forms import ConfigForm, BankFormSet, CompanyAtmLocationFormSet, XFSFormatForm
from atm_analytics.companies.models import Company, CompanyAtmLocation, Bank, AtmRepositionEvent, XFSFormat, \
    XFSFormatEvent


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


@login_required(login_url='/login')
def create_xfs_format(request):
    user = request.user.dash_user
    company = Company.objects.get(users=user)
    form = XFSFormatForm()

    if request.method == 'POST':
        form = XFSFormatForm(request.POST, request.FILES)
        if form.is_valid():
            xfs_format = form.save(commit=False)
            xfs_format.company = company
            xfs_format.save()

            critical_errors_list = request.POST["critical-errors-list"].split(",")
            important_errors_list = request.POST["important-errors-list"].split(",")
            no_errors_list = request.POST["no-errors-list"].split(",")

            if len(critical_errors_list) > 0:
                for item in critical_errors_list:
                    if item == "":
                        continue
                    XFSFormatEvent.objects.get_or_create(
                        xfs_format=xfs_format,
                        pattern=item,
                        type=XFSFormatEvent.EVENT_TYPE_CRITICAL_ERROR)

            if len(important_errors_list) > 0:
                for item in important_errors_list:
                    if item == "":
                        continue
                    XFSFormatEvent.objects.get_or_create(
                        xfs_format=xfs_format,
                        pattern=item,
                        type=XFSFormatEvent.EVENT_TYPE_IMPORTANT_ERROR)

            if len(no_errors_list) > 0:
                for item in no_errors_list:
                    if item == "":
                        continue
                    XFSFormatEvent.objects.get_or_create(
                        xfs_format=xfs_format,
                        pattern=item,
                        type=XFSFormatEvent.EVENT_TYPE_NO_ERROR)

            return HttpResponseRedirect(
                reverse("companies:update_xfs_format", args=[xfs_format.id]))

    return render(request, 'companies/xfs_format.html', {
        'form': form
    })


@login_required(login_url='/login')
def update_xfs_format(request, xfs_format_id):
    xfs_format = XFSFormat.objects.get(id=xfs_format_id)
    xfs_sample_file_txt = xfs_format.xfs_sample_file.file.read()
    xfs_sample_file_txt = try_unicode(xfs_sample_file_txt)

    user = request.user.dash_user
    company = Company.objects.get(users=user)
    form = XFSFormatForm(instance=xfs_format)

    if request.method == 'POST':
        form = XFSFormatForm(request.POST, request.FILES, instance=xfs_format)
        if form.is_valid():
            xfs_format = form.save(commit=False)
            xfs_format.company = company

            critical_errors_list = request.POST["critical-errors-list"].split(",")
            important_errors_list = request.POST["important-errors-list"].split(",")
            no_errors_list = request.POST["no-errors-list"].split(",")
            xfs_format.save()

            XFSFormatEvent.objects.filter(xfs_format=xfs_format).delete()

            if len(critical_errors_list) > 0:
                for item in critical_errors_list:
                    if item == "":
                        continue
                    XFSFormatEvent.objects.get_or_create(
                        xfs_format=xfs_format,
                        pattern=item,
                        type=XFSFormatEvent.EVENT_TYPE_CRITICAL_ERROR)

            if len(important_errors_list) > 0:
                for item in important_errors_list:
                    if item == "":
                        continue
                    XFSFormatEvent.objects.get_or_create(
                        xfs_format=xfs_format,
                        pattern=item,
                        type=XFSFormatEvent.EVENT_TYPE_IMPORTANT_ERROR)

            if len(no_errors_list) > 0:
                for item in no_errors_list:
                    if item == "":
                        continue
                    XFSFormatEvent.objects.get_or_create(
                        xfs_format=xfs_format,
                        pattern=item,
                        type=XFSFormatEvent.EVENT_TYPE_NO_ERROR)

    xfs_format_events = {
        "critical_errors": list(XFSFormatEvent.objects.filter(
            xfs_format=xfs_format, type=XFSFormatEvent.EVENT_TYPE_CRITICAL_ERROR).values_list('pattern', flat=True)),
        "important_errors": list(XFSFormatEvent.objects.filter(
            xfs_format=xfs_format, type=XFSFormatEvent.EVENT_TYPE_IMPORTANT_ERROR).values_list('pattern', flat=True)),
        "no_errors": list(XFSFormatEvent.objects.filter(
            xfs_format=xfs_format, type=XFSFormatEvent.EVENT_TYPE_NO_ERROR).values_list('pattern', flat=True))
    }

    return render(request, 'companies/xfs_format.html', {
        'form': form,
        'can_delete': True,
        'xfs_sample_file_txt': xfs_sample_file_txt,
        'xfs_format_events': xfs_format_events,
    })


@login_required(login_url='/login')
def delete_xfs_format(request, xfs_format_id):
    xfs_format = get_object_or_404(XFSFormat, id=xfs_format_id)
    xfs_format.delete()
    return HttpResponseRedirect(reverse("base:dashboard"))
