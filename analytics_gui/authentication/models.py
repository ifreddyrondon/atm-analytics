# coding=utf-8

from django.conf import settings
from django.db import models


class UserDashboard(models.Model):
    POSITION_ANALYST = '0'
    POSITION_ADMIN = '1'
    POSITIONS_CHOICES = (
        (POSITION_ANALYST, "analista"),
        (POSITION_ADMIN, "admin"),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="dash_user")
    position = models.CharField(
            max_length=1,
            choices=POSITIONS_CHOICES)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = "Usuario"
