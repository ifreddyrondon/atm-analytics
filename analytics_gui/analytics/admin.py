from django.contrib import admin

from analytics_gui.analytics.models import Case, AtmCase, AtmError

admin.site.register(Case)
admin.site.register(AtmCase)
admin.site.register(AtmError)
