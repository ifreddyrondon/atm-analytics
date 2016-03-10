# coding=utf-8

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from analytics_gui.companies.models import Company


class UserDashboard(models.Model):
    POSITION_ANALYST = '0'
    POSITION_ADMIN = '1'
    POSITIONS_CHOICES = (
        (POSITION_ANALYST, _("analyst")),
        (POSITION_ADMIN, _("manager")),
    )

    user = models.OneToOneField(
        User, related_name="dash_user")
    company = models.ForeignKey(
        Company, related_name='users', verbose_name=_("Company"))
    charge = models.CharField("Cargo", max_length=1, choices=POSITIONS_CHOICES)
    position = models.PositiveSmallIntegerField(
        _("position"), null=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = _("User")
