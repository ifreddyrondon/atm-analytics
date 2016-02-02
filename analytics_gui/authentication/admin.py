# coding=utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from analytics_gui.authentication.models import UserDashboard
from analytics_gui.companies.models import Company


class UserDashboardAdmin(admin.ModelAdmin):
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


admin.site.register(UserDashboard, UserDashboardAdmin)


class UserDashboardInline(admin.TabularInline):
    model = UserDashboard


class UserAdmin(UserAdmin):
    inlines = [UserDashboardInline, ]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
