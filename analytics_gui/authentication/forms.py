# coding=utf-8
from django import forms

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


class CustomAuthenticationForm(forms.Form):

    username = forms.CharField(
        max_length=254,
        error_messages=default_errors,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nombre de usuario',
                'class': 'form-control'
            }
        )
    )

    password = forms.CharField(
        error_messages=default_errors,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].error_messages = default_errors