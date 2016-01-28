from django.contrib import admin
from grappelli.forms import GrappelliSortableHiddenMixin

from analytics_gui.authentication.models import CompanyAtmLocation, Company, Bank


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


admin.site.register(Company, CompanyAdmin)
