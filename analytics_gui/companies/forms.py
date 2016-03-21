# coding=utf-8
from django import forms
from django.forms import inlineformset_factory

from analytics_gui.companies.models import Company, Bank, CompanyAtmLocation


class ConfigForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('logo', 'name', 'email', 'phone')


class BankForm(forms.ModelForm):
    atms_number = forms.IntegerField(min_value=1)

    class Meta:
        model = Bank
        fields = ['name', 'atms_number']


BankFormSet = inlineformset_factory(
    Company,
    Bank,
    form=BankForm,
    extra=0,
    min_num=1,
    max_num=1,
)


class CompanyAtmLocationForm(forms.ModelForm):
    class Meta:
        model = CompanyAtmLocation
        fields = ['address']


CompanyAtmLocationFormSet = inlineformset_factory(
    Company,
    CompanyAtmLocation,
    form=CompanyAtmLocationForm,
    extra=0,
    min_num=1,
    max_num=1,
)
