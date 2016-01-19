from django.contrib import admin

from analytics_gui.analytics.models import Case, AtmCase, Company, CompanyAtmLocation


class CompanyAtmLocationInline(admin.TabularInline):
    model = CompanyAtmLocation
    extra = 1


class CompanyAdmin(admin.ModelAdmin):
    inlines = (CompanyAtmLocationInline, )


admin.site.register(Company, CompanyAdmin)
admin.site.register(Case)
admin.site.register(AtmCase)
