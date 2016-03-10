# coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _


class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('User name'),
                'class': 'form-control'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Password'),
                'class': 'form-control'
            }
        )
    )


class CreateAnalystForm(forms.Form):
    first_name = forms.CharField(
        help_text=_('First name'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('First name'),
                'class': 'form-control'
            }
        )
    )

    last_name = forms.CharField(
        help_text=_('Last name'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Last name'),
                'class': 'form-control'
            }
        )
    )

    email = forms.EmailField(
        help_text=_('Email'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Email'),
                'class': 'form-control'
            }
        )
    )

    username = forms.CharField(
        help_text=_('Username'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Username'),
                'class': 'form-control'
            }
        )
    )

    password = forms.CharField(
        help_text=_('Password'),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Password'),
                'class': 'form-control'
            }
        )
    )