# coding=utf-8
from django import forms
from django.forms import inlineformset_factory

from analytics_gui.companies.models import Company, Bank, CompanyAtmLocation

default_errors = {
    u'required': u"Este campo es requerido",
    u'invalid': u"Coloca un valor válido",
    u'inactive': u"Esta cuenta esta inactiva",
    u'invalid_login': u"Por favor coloca el usuario y clave correcta",
    u'email_not_exists': u"No existe usuario con este correo electrónico",
    u'password_incorrect': u"La contraseña introducida es incorrecta. Intenta nuevamente",
    u'password_mismatch': u"Las contraseñas no coinciden",
    u'unknown': u"Ese usuario no tiene una cuenta asociada.",
}


class ConfigForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('logo', 'name', 'email', 'phone')

    def __init__(self, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].error_messages = default_errors


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
        min_num=0,
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
        min_num=0,
        max_num=1,
)
