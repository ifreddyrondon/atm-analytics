# coding=utf-8

from django.contrib.auth.models import User
from django.db import models

from analytics_gui.companies.models import Company


class UserDashboard(models.Model):
    POSITION_ANALYST = '0'
    POSITION_ADMIN = '1'
    POSITIONS_CHOICES = (
        (POSITION_ANALYST, "analista"),
        (POSITION_ADMIN, "manager"),
    )

    user = models.OneToOneField(User, related_name="dash_user")
    company = models.ForeignKey(Company, related_name='users', verbose_name='Compañia')
    charge = models.CharField("Cargo", max_length=1, choices=POSITIONS_CHOICES)
    position = models.PositiveSmallIntegerField("Posición", null=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = "Usuario"
