from django.contrib import admin

from analytics_gui.analytics.models import Case, AtmCase, AtmErrorEventViewer, AtmErrorXFS

admin.site.register(Case)
admin.site.register(AtmCase)
admin.site.register(AtmErrorXFS)
admin.site.register(AtmErrorEventViewer)
