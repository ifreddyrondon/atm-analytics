# coding=utf-8
from django import forms

from analytics_gui.companies.models import Company

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
