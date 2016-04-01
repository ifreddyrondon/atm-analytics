# coding=utf-8
import os

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


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
        verbose_name_plural = _("Companies")


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


def get_xfs_samples_attachment_path(instance, filename):
    return os.path.join(
        'xfs_samples',
        str(timezone.now()),
        filename
    )


class XFSFormat(models.Model):
    HARDWARE_DIEBOLD = '0'
    HARDWARE_WINCOR_NIXDORF = '1'
    HARDWARE_NCR = '2'
    HARDWARE_TRISTON = '3'
    HARDWARE_CHOICES = (
        (HARDWARE_DIEBOLD, "Diebold"),
        (HARDWARE_WINCOR_NIXDORF, "Wincor Nixdorf"),
        (HARDWARE_NCR, "NCR"),
        (HARDWARE_TRISTON, "Triton"),
    )

    SOFTWARE_AGILIS = '0'
    SOFTWARE_APTRA = '1'
    SOFTWARE_PROCASH_PROBASE = '2'
    SOFTWARE_JAM_DYNASTY = '3'
    SOFTWARE_KAL = '4'
    SOFTWARE_OTRO = '5'
    SOFTWARE_CHOICES = (
        (SOFTWARE_AGILIS, "Agilis"),
        (SOFTWARE_APTRA, "APTRA"),
        (SOFTWARE_PROCASH_PROBASE, "Procash/probase"),
        (SOFTWARE_JAM_DYNASTY, "JAM Dynasty"),
        (SOFTWARE_KAL, "Kal"),
        (SOFTWARE_OTRO, _("Other XFS")),
    )

    hardware = models.CharField(
        max_length=1,
        choices=HARDWARE_CHOICES,
        help_text=_("Hardware"),
    )

    software = models.CharField(
        max_length=1,
        choices=SOFTWARE_CHOICES,
        help_text=_("Software"),
    )

    xfs_sample_file = models.FileField(
        _("XFS sample file"), upload_to=get_xfs_samples_attachment_path)

    group_separator = models.CharField(_("Group Separator"), max_length=255)
    row_separator = models.CharField(_("Row Separator"), max_length=255)
    date_pattern = models.CharField(
        _("Date pattern"), max_length=255,
        help_text=_('Select any "date-time" inside the text'),
    )
    total_amount_pattern = models.CharField(_("Total amount pattern"), max_length=255)
    currency_pattern = models.CharField(
        _("Currency pattern"), max_length=255, null=True, blank=True)

    company = models.ForeignKey(Company)
    position = models.PositiveSmallIntegerField(_("Position"), null=True)

    class Meta:
        ordering = ['position']
        verbose_name = _("XFS Formats")

    def __unicode__(self):
        return "{} - {}".format(self.hardware, self.software)


class XFSFormatEvent(models.Model):
    EVENT_TYPE_CRITICAL_ERROR = '0'
    EVENT_TYPE_IMPORTANT_ERROR = '1'
    EVENT_TYPE_NO_ERROR = '2'
    EVENT_TYPES = (
        (EVENT_TYPE_CRITICAL_ERROR, "Critical erros"),
        (EVENT_TYPE_IMPORTANT_ERROR, "Important error"),
        (EVENT_TYPE_NO_ERROR, "No error"),
    )

    xfs_format = models.ForeignKey(XFSFormat)
    pattern = models.CharField(max_length=255)
    type = models.CharField(
        max_length=1,
        choices=EVENT_TYPES,
        help_text=_("Type of event"),
    )


class AtmRepositionEvent(models.Model):
    bank = models.ForeignKey(Bank)
    location = models.ForeignKey(CompanyAtmLocation)
    reposition_date = models.DateTimeField()
