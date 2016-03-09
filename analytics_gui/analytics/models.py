import os

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from analytics_gui.analytics.choices import CURRENCY_CHOICES
from analytics_gui.authentication.models import UserDashboard
from analytics_gui.companies.models import Bank, CompanyAtmLocation


def get_case_picture_path(instance, filename):
    return os.path.join(
        'company',
        'case',
        filename
    )


class Case(models.Model):
    PRIORITY_LOW = '0'
    PRIORITY_MEDIUM = '1'
    PRIORITY_HIGH = '2'
    PRIORITY_CHOICES = (
        (PRIORITY_LOW, _("low")),
        (PRIORITY_MEDIUM, _("medium")),
        (PRIORITY_HIGH, _("high")),
    )

    STATUS_OPEN = '0'
    STATUS_CLOSE = '1'
    STATUS_CHOICES = (
        (STATUS_OPEN, _("open")),
        (STATUS_CLOSE, _("close")),
    )

    number = models.IntegerField(
        db_index=True,
        help_text=_("Case number")
    )

    picture = models.ImageField(upload_to=get_case_picture_path, null=True, blank=True)

    name = models.CharField(max_length=255, help_text=_('Case name'))
    priority = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        help_text=_('Importance of the case')
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
        help_text=_('Case status')
    )
    created_date = models.DateField(
        null=True, blank=True,
        help_text=_('Creation date of the case')
    )

    missing_amount = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        help_text=_("Estimated amount missing")
    )

    missing_amount_currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        help_text=_('Currency')
    )

    description = models.TextField(
        null=True, blank=True,
        help_text=_("Extra brief description of the case")
    )

    resolution = models.TextField(null=True, blank=True)

    bank = models.ForeignKey(
        Bank,
        related_name="bank_cases",
        help_text=_("Bank"))

    analyst = models.ForeignKey(
        UserDashboard,
        related_name="analyst_cases")

    @staticmethod
    def get_case_number():
        top = Case.objects.order_by('-number')
        return top[0].number + 1 if len(top) > 0 else 0

    def save(self, **kwargs):
        """Get last value of Number from database, and increment before save
        :param **kwargs:
        """
        if not self.number:
            self.number = self.get_case_number()

        super(Case, self).save()

    def __unicode__(self):
        return "{} - {}".format(self.number, self.name)

    class Meta:
        verbose_name = _("Case")


def get_atm_errors_manual_attachment_path(instance, filename):
    return os.path.join(
        'atm',
        'errors_manual',
        str(timezone.now()),
        filename
    )


def get_atm_microsoft_event_viewer_attachment_path(instance, filename):
    return os.path.join(
        'atm',
        'microsoft_event_viewer',
        str(timezone.now()),
        filename
    )


def get_atm_other_log_attachment_path(instance, filename):
    return os.path.join(
        'atm',
        'other_log',
        str(timezone.now()),
        filename
    )


class AtmCase(models.Model):
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

    OS_WINDOWS_XP = '0'
    OS_WINDOWS_7 = '1'
    OS_WINDOWS_8 = '2'
    OS_CHOICES = (
        (OS_WINDOWS_XP, "Windows XP"),
        (OS_WINDOWS_7, "Windows 7"),
        (OS_WINDOWS_8, "Windows 8"),
    )

    case = models.ForeignKey(Case, related_name="atms")

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

    operating_system = models.CharField(
        max_length=1,
        choices=OS_CHOICES,
        help_text=_("Operating system"),
    )

    errors_manual = models.FileField(
        null=True, blank=True,
        upload_to=get_atm_errors_manual_attachment_path
    )

    microsoft_event_viewer = models.FileField(
        null=True, blank=True,
        upload_to=get_atm_microsoft_event_viewer_attachment_path
    )

    person_name_journal_virtual = models.CharField(
        max_length=255,
        help_text=_('Name of the person who facilitates the virtual Journal'))

    other_log = models.FileField(
        null=True, blank=True,
        upload_to=get_atm_other_log_attachment_path,
        help_text=_("Another type of log?")
    )

    atm_location = models.ManyToManyField(
        CompanyAtmLocation,
        related_name="locations",
        help_text=_("ATM location")
    )

    def __unicode__(self):
        return _('%(hardware), %(software) and %(OS)') % {'hardware': self.hardware, 'software': self.software,
                                                          'OS': self.operating_system}

    class Meta:
        verbose_name = _("ATM")
        verbose_name_plural = _("ATMs")


def get_atm_journal_virtual_attachment_path(instance, filename):
    return os.path.join(
        'atm',
        'journal_virtual',
        str(timezone.now().date()),
        filename
    )


class AtmJournal(models.Model):
    atm = models.ForeignKey(AtmCase, related_name="journals")
    file = models.FileField(
        upload_to=get_atm_journal_virtual_attachment_path,
    )

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def __unicode__(self):
        return self.filename


class AtmErrorXFS(models.Model):
    class Meta:
        verbose_name = _("XFS Error")
        verbose_name_plural = _("XFS Errors")

    ERROR_COLOR_GREEN = settings.COLOR_GREEN
    ERROR_COLOR_RED = settings.COLOR_RED
    ERROR_COLOR_ORANGE = settings.COLOR_ORANGE
    ERRORS_COLORS_CHOICES = (
        (ERROR_COLOR_GREEN, _("green")),
        (ERROR_COLOR_RED, _("red")),
        (ERROR_COLOR_ORANGE, _("orange")),
    )

    ERROR_FAULT_USER = '0'
    ERROR_FAULT_BANK = '1'
    ERROR_FAULT_TRANSVALORES = '2'
    ERROR_FAULT_ANONYMOUS = '3'
    ERROR_FAULT_CHOICES = (
        (ERROR_FAULT_USER, _("user")),
        (ERROR_FAULT_BANK, _("bank")),
        (ERROR_FAULT_BANK, _("transporting company")),
        (ERROR_FAULT_ANONYMOUS, _("anonymous")),
    )

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

    OS_WINDOWS_XP = '0'
    OS_WINDOWS_7 = '1'
    OS_WINDOWS_8 = '2'
    OS_CHOICES = (
        (OS_WINDOWS_XP, "Windows XP"),
        (OS_WINDOWS_7, "Windows 7"),
        (OS_WINDOWS_8, "Windows 8"),
    )

    identifier = models.CharField(
        _("Identifier"),
        max_length=255,
        unique=True,
        db_index=True,
        help_text=_("Unique identifier of the error"),
    )

    description = models.CharField(
        _("Description"),
        max_length=255,
        help_text=_("Description of error"),
    )

    hardware = models.CharField(
        _("Hardware"),
        max_length=1,
        choices=HARDWARE_CHOICES,
        help_text=_("ATM hardware"),
    )

    software = models.CharField(
        _("Software"),
        max_length=1,
        choices=SOFTWARE_CHOICES,
        help_text=_("ATM software"),
    )

    operating_system = models.CharField(
        _("Operating System"),
        max_length=1,
        choices=OS_CHOICES,
        help_text=_("ATM Operating System"),
    )

    fault = models.CharField(
        _("Guilt"),
        max_length=1,
        choices=ERROR_FAULT_CHOICES,
        help_text=_("Who is guilty?"),
    )

    color = models.CharField(
        _("Color"),
        max_length=1,
        choices=ERRORS_COLORS_CHOICES,
        help_text=_("Error color"),
    )


class AtmErrorEventViewer(models.Model):
    class Meta:
        verbose_name = _("EventViewer Error")
        verbose_name_plural = _("EventViewer Errors")

    ERROR_COLOR_GREEN = settings.COLOR_GREEN
    ERROR_COLOR_RED = settings.COLOR_RED
    ERROR_COLOR_ORANGE = settings.COLOR_ORANGE
    ERRORS_COLORS_CHOICES = (
        (ERROR_COLOR_GREEN, _("green")),
        (ERROR_COLOR_RED, _("red")),
        (ERROR_COLOR_ORANGE, _("orange")),
    )

    OS_WINDOWS_XP = '0'
    OS_WINDOWS_7 = '1'
    OS_WINDOWS_8 = '2'
    OS_CHOICES = (
        (OS_WINDOWS_XP, "Windows XP"),
        (OS_WINDOWS_7, "Windows 7"),
        (OS_WINDOWS_8, "Windows 8"),
    )

    identifier = models.CharField(
        _("Identifier"),
        max_length=255,
        unique=True,
        db_index=True,
        help_text=_("Unique identifier of the error"),
    )

    description = models.CharField(
        _("Description"),
        max_length=255,
        help_text=_("Description of error"),
    )

    operating_system = models.CharField(
        _("Operating System"),
        max_length=1,
        choices=OS_CHOICES,
        help_text=_("ATM Operating System"),
    )

    color = models.CharField(
        _("Color"),
        max_length=1,
        choices=ERRORS_COLORS_CHOICES,
        help_text=_("Error color"),
    )


class AtmEventViewerEvent(models.Model):
    class Meta:
        ordering = ['event_date']

    atm = models.ForeignKey(AtmCase, related_name="event_viewer_errors")

    event_id = models.CharField(max_length=255)

    event_record_id = models.CharField(max_length=255)

    event_date = models.DateTimeField(_("Date of the event"))

    context = models.TextField()
