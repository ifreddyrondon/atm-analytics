from django.contrib import admin
from django.utils.translation import ugettext as _
from grappelli.forms import GrappelliSortableHiddenMixin

from atm_analytics.authentication.models import UserDashboard
from atm_analytics.companies.models import CompanyAtmLocation, Bank, Company


class UserDashboardInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    classes = ('grp-collapse grp-open',)
    model = UserDashboard
    extra = 1
    sortable_field_name = "position"


class CompanyBankInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    classes = ('grp-collapse grp-open',)
    model = Bank
    extra = 1
    sortable_field_name = "position"


class CompanyAtmLocationInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    classes = ('grp-collapse grp-open',)
    model = CompanyAtmLocation
    extra = 1
    sortable_field_name = "position"


class CompanyAdmin(admin.ModelAdmin):
    inlines = (UserDashboardInline, CompanyBankInline, CompanyAtmLocationInline,)
    list_display = ('name', 'banks_list', 'atm_number_4_bank',)

    def banks_list(self, obj):
        li = '<ul>'
        for bank in obj.banks.all():
            li += '<li>{}</li>'.format(bank.name)
        li += '</ul>'
        return li

    banks_list.allow_tags = True
    banks_list.short_description = _('Banks')

    def atm_number_4_bank(self, obj):
        li = '<ul>'
        for bank in obj.banks.all():
            li += '<li>{}</li>'.format(bank.atms_number)
        li += '</ul>'
        return li

    atm_number_4_bank.allow_tags = True
    atm_number_4_bank.short_description = _("Number of ATMs")


admin.site.register(Company, CompanyAdmin)
