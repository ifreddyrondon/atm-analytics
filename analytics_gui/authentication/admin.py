# coding=utf-8
from django.contrib import admin
from grappelli.forms import GrappelliSortableHiddenMixin

from analytics_gui.authentication.models import CompanyAtmLocation, Company, Bank, UserDashboard


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
    inlines = (CompanyBankInline, CompanyAtmLocationInline,)
    list_display = ('name', 'banks_list', 'atm_number_4_bank', )

    def banks_list(self, obj):
        li = '<ul>'
        for bank in obj.banks.all():
            li += '<li>{}</li>'.format(bank.name)
        li += '</ul>'
        return li
    banks_list.allow_tags = True
    banks_list.short_description = 'Bancos'

    def atm_number_4_bank(self, obj):
        li = '<ul>'
        for bank in obj.banks.all():
            li += '<li>{}</li>'.format(bank.atms_number)
        li += '</ul>'
        return li
    atm_number_4_bank.allow_tags = True
    atm_number_4_bank.short_description = 'Cantidad de ATMs'


admin.site.register(Company, CompanyAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ('users_list', 'position_list', 'company')

    def users_list(self, obj):
        return obj.user.username
    users_list.short_description = 'Usuario'

    def position_list(self, obj):
        return obj.get_position_display()
    position_list.short_description = 'Posición'

    def company(self, obj):
        if obj.position == UserDashboard.POSITION_ADMIN:
            return Company.objects.get(in_charge=obj)
        elif obj.position == UserDashboard.POSITION_ANALYST:
            return Company.objects.get(users=obj)
    company.short_description = 'Compañia'

admin.site.register(UserDashboard, UserAdmin)
