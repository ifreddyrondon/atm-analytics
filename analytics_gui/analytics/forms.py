# coding=utf-8
from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet

from analytics_gui.analytics.models import Case, AtmCase
from analytics_gui.companies.models import Bank, CompanyAtmLocation

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


class CreateCaseForm(forms.ModelForm):
    number = forms.IntegerField(
            help_text='Número de caso',
            min_value=0,
            required=False,
            widget=forms.TextInput(attrs={'placeholder': str(Case.get_case_number())})
    )

    priority = forms.ChoiceField(
            widget=forms.RadioSelect,
            choices=Case.PRIORITY_CHOICES,
            help_text='Importancia del caso'
    )

    status = forms.ChoiceField(
            widget=forms.RadioSelect,
            choices=Case.STATUS_CHOICES,
            help_text='Estado del caso'
    )

    created_date = forms.DateField(
            input_formats=['%d-%m-%Y', ],
            widget=forms.DateInput(format='%d-%m-%Y'),
            help_text='Fecha de creación del caso',
    )

    class Meta:
        model = Case
        fields = (
            'number', 'name', 'priority', 'status', 'created_date',
            'missing_amount', 'bank', 'description',
        )

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super(CreateCaseForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].error_messages = default_errors

        self.fields['bank'].queryset = Bank.objects.filter(company=company)


class BaseAtmFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super(BaseAtmFormSet, self).__init__(*args, **kwargs)

        initial = [{'company': company}]
        self.initial = initial
        # Make enough extra formsets to hold initial forms
        self.extra += len(initial)


class CreateAtmForm(forms.ModelForm):
    class Meta:
        model = AtmCase
        fields = (
            'hardware', 'software', 'operating_system', 'errors_manual',
            'microsoft_event_viewer', 'cash_replacement_schedule',
            'person_name_journal_virtual', 'other_log',
            'atm_location',
        )

    def __init__(self, *args, **kwargs):
        super(CreateAtmForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].error_messages = default_errors

        if kwargs.get('initial'):
            self.fields['atm_location'].queryset = CompanyAtmLocation.objects.filter(
                company=kwargs.get('initial').get('company'))


CreateAtmFormSet = inlineformset_factory(
        Case,
        AtmCase,
        formset=BaseAtmFormSet,
        form=CreateAtmForm,
        extra=0,
        min_num=1
)
