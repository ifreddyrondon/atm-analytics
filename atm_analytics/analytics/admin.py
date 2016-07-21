from django.contrib import admin

from atm_analytics.analytics.models import Case, AtmCase, AtmErrorEventViewer, AtmErrorXFS, AtmJournal


class AtmJournalInline(admin.TabularInline):
    classes = ('grp-collapse grp-open',)
    model = AtmJournal
    extra = 0


class AtmCaseAdmin(admin.ModelAdmin):
    inlines = (AtmJournalInline,)


class AtmCaseInline(admin.TabularInline):
    classes = ('grp-collapse grp-open',)
    model = AtmCase
    extra = 0


class CaseAdmin(admin.ModelAdmin):
    inlines = (AtmCaseInline,)


admin.site.register(AtmCase, AtmCaseAdmin)
admin.site.register(Case, CaseAdmin)
admin.site.register(AtmErrorXFS)
admin.site.register(AtmErrorEventViewer)
