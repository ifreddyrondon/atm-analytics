# coding=utf-8
from django.contrib import admin

from atm_analytics.authentication.models import UserDashboard
from atm_analytics.companies.models import Company


class UserDashboardAdmin(admin.ModelAdmin):
    list_display = ('users_list', 'position_list', 'company')

    def users_list(self, obj):
        return obj.user.username

    users_list.short_description = 'Usuario'

    def position_list(self, obj):
        return obj.get_charge_display()

    position_list.short_description = 'Cargo'

    def company(self, obj):
        if obj.position == UserDashboard.POSITION_ADMIN:
            return Company.objects.get(in_charge=obj)
        elif obj.position == UserDashboard.POSITION_ANALYST:
            return Company.objects.get(users=obj)

    company.short_description = 'Compañia'


admin.site.register(UserDashboard, UserDashboardAdmin)
