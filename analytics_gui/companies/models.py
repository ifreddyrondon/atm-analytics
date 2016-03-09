# coding=utf-8
import os

from django.db import models
from django.utils.translation import ugettext as _


def get_company_logo_attachment_path(instance, filename):
    return os.path.join(
            'company',
            'logo',
            filename
    )


class Company(models.Model):
    logo = models.ImageField(upload_to=get_company_logo_attachment_path, null=True, blank=True)
    name = models.CharField(
        _('Name'), max_length=255, help_text=_('Company name'))
    email = models.EmailField(
        _('Email'), max_length=255, help_text=_('Email'))
    phone = models.CharField(
        _('Phone'), max_length=255, help_text=_('Phone number'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Company")


class Bank(models.Model):
    name = models.CharField(
        _('Name'), max_length=255, help_text=_('Bank name'))
    atms_number = models.IntegerField(
        'ATMs', help_text=_('Number of ATMs'))
    company = models.ForeignKey(Company, related_name="banks")
    position = models.PositiveSmallIntegerField(_("Position"), null=True)

    class Meta:
        ordering = ['position']
        verbose_name = _("Bank")

    def __unicode__(self):
        return self.name


class CompanyAtmLocation(models.Model):
    address = models.CharField(_("Address"), max_length=255)
    company = models.ForeignKey(Company)
    position = models.PositiveSmallIntegerField(_("Position"), null=True)

    class Meta:
        ordering = ['position']
        verbose_name = _("ATM address")

    def __unicode__(self):
        return self.address


class AtmRepositionEvent(models.Model):
    bank = models.ForeignKey(Bank)
    location = models.ForeignKey(CompanyAtmLocation)
    reposition_date = models.DateTimeField()
