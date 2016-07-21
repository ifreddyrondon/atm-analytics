from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _

from atm_analytics.analytics.models import Case, AtmCase
from atm_analytics.companies.models import Bank, CompanyAtmLocation


class CreateCaseForm(forms.ModelForm):
    number = forms.IntegerField(
        help_text=_('Case number'),
        min_value=0,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': str(Case.get_case_number())})
    )

    priority = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=Case.PRIORITY_CHOICES,
        help_text=_('Importance of the case')
    )

    status = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=Case.STATUS_CHOICES,
        initial=Case.STATUS_OPEN,
        help_text=_('Case status')
    )

    created_date = forms.DateField(
        input_formats=['%d-%m-%Y', ],
        widget=forms.DateInput(format='%d-%m-%Y'),
        help_text=_('Creation date of the case'),
    )

    class Meta:
        model = Case
        fields = (
            'picture', 'number', 'name', 'priority', 'status', 'created_date',
            'missing_amount', 'missing_amount_currency', 'bank', 'description',
        )

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super(CreateCaseForm, self).__init__(*args, **kwargs)

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
            'microsoft_event_viewer', 'person_name_journal_virtual',
            'other_log', 'atm_location',
        )

    def __init__(self, *args, **kwargs):
        super(CreateAtmForm, self).__init__(*args, **kwargs)

        if kwargs.get('initial'):
            self.fields['atm_location'].queryset = CompanyAtmLocation.objects.filter(
                company=kwargs.get('initial').get('company'))


CreateAtmFormSet = inlineformset_factory(
    Case,
    AtmCase,
    formset=BaseAtmFormSet,
    form=CreateAtmForm,
    extra=0,
    min_num=0,
    max_num=1,
)


class AnalyticForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ('resolution',)

    def __init__(self, *args, **kwargs):
        super(AnalyticForm, self).__init__(*args, **kwargs)

        self.fields['resolution'].required = True
