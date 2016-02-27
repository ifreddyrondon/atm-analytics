# coding=utf-8
import os

from django.conf import settings
from django.db import models
from django.utils import timezone

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
        (PRIORITY_LOW, "bajo"),
        (PRIORITY_MEDIUM, "medio"),
        (PRIORITY_HIGH, "alto"),
    )

    STATUS_OPEN = '0'
    STATUS_CLOSE = '1'
    STATUS_CHOICES = (
        (STATUS_OPEN, "abierto"),
        (STATUS_CLOSE, "cerrado"),
    )

    number = models.IntegerField(
            db_index=True,
            help_text='Número de caso'
    )

    picture = models.ImageField(upload_to=get_case_picture_path, null=True, blank=True)

    name = models.CharField(max_length=255, help_text='Nombre del caso')
    priority = models.CharField(
            max_length=1,
            choices=PRIORITY_CHOICES,
            help_text='Importancia del caso'
    )
    status = models.CharField(
            max_length=1,
            choices=STATUS_CHOICES,
            default=STATUS_OPEN,
            help_text='Estado del caso'
    )
    created_date = models.DateField(
            null=True, blank=True,
            help_text='Fecha de creación del caso'
    )

    missing_amount = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            help_text="Monto faltante estimado"
    )

    missing_amount_currency = models.CharField(
            max_length=3,
            choices=CURRENCY_CHOICES,
            help_text='Divisa'
    )

    description = models.TextField(
            null=True, blank=True,
            help_text="Breve descripción extra del caso"
    )

    resolution = models.TextField(null=True, blank=True)

    bank = models.ForeignKey(
            Bank, related_name="bank_cases", help_text="Banco")
    analyst = models.ForeignKey(UserDashboard, related_name="analyst_cases")

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
        verbose_name = "Caso"


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


def get_atm_cash_replacement_schedule_attachment_path(instance, filename):
    return os.path.join(
            'atm',
            'cash_replacement_schedule',
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
        (SOFTWARE_OTRO, "Otro XFS"),
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
            help_text="Hardware",
    )

    software = models.CharField(
            max_length=1,
            choices=SOFTWARE_CHOICES,
            help_text="Software",
    )

    operating_system = models.CharField(
            max_length=1,
            choices=OS_CHOICES,
            help_text="Sistema Operativo",
    )

    errors_manual = models.FileField(
            null=True, blank=True,
            upload_to=get_atm_errors_manual_attachment_path
    )

    microsoft_event_viewer = models.FileField(
            null=True, blank=True,
            upload_to=get_atm_microsoft_event_viewer_attachment_path
    )

    cash_replacement_schedule = models.FileField(
            null=True, blank=True,
            upload_to=get_atm_cash_replacement_schedule_attachment_path
    )

    person_name_journal_virtual = models.CharField(
            max_length=255,
            help_text='Nombre de la persona que le facilito el Journal virtual')

    other_log = models.FileField(
            null=True, blank=True,
            upload_to=get_atm_other_log_attachment_path,
            help_text="¿Otro tipo de log?"
    )

    atm_location = models.ManyToManyField(
            CompanyAtmLocation,
            related_name="locations",
            help_text="Localización del ATM"
    )

    def __unicode__(self):
        return "{}, {} and {}".format(self.hardware, self.software, self.operating_system)

    class Meta:
        verbose_name = "ATM"
        verbose_name_plural = "ATMs"


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
        verbose_name = "Error XFS"
        verbose_name_plural = "Errores XFS"

    ERROR_COLOR_GREEN = settings.COLOR_GREEN
    ERROR_COLOR_RED = settings.COLOR_RED
    ERROR_COLOR_ORANGE = settings.COLOR_ORANGE
    ERRORS_COLORS_CHOICES = (
        (ERROR_COLOR_GREEN, "verde"),
        (ERROR_COLOR_RED, "rojo"),
        (ERROR_COLOR_ORANGE, "naranja"),
    )

    ERROR_FAULT_USER = '0'
    ERROR_FAULT_BANK = '1'
    ERROR_FAULT_TRANSVALORES = '2'
    ERROR_FAULT_ANONYMOUS = '3'
    ERROR_FAULT_CHOICES = (
        (ERROR_FAULT_USER, "usuario"),
        (ERROR_FAULT_BANK, "banco"),
        (ERROR_FAULT_BANK, "transvalores"),
        (ERROR_FAULT_ANONYMOUS, "anonimo"),
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
        (SOFTWARE_OTRO, "Otro XFS"),
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
            "Identificador",
            max_length=255,
            unique=True,
            db_index=True,
            help_text="Identificador único del error",
    )

    description = models.CharField(
            "Descripción",
            max_length=255,
            help_text="Descripción del error",
    )

    hardware = models.CharField(
            "Hardware",
            max_length=1,
            choices=HARDWARE_CHOICES,
            help_text="Hardware del ATM",
    )

    software = models.CharField(
            "Software",
            max_length=1,
            choices=SOFTWARE_CHOICES,
            help_text="Software del ATM",
    )

    operating_system = models.CharField(
            "Sistema Operativo",
            max_length=1,
            choices=OS_CHOICES,
            help_text="Sistema Operativo del ATM",
    )

    fault = models.CharField(
            "Culpa",
            max_length=1,
            choices=ERROR_FAULT_CHOICES,
            help_text="¿Quién tiene la culpa?",
    )

    color = models.CharField(
            "Color",
            max_length=1,
            choices=ERRORS_COLORS_CHOICES,
            help_text="Color del error",
    )


class AtmErrorEventViewer(models.Model):
    class Meta:
        verbose_name = "Error de EventViewer"
        verbose_name_plural = "Errores de EventViewer"

    ERROR_COLOR_GREEN = settings.COLOR_GREEN
    ERROR_COLOR_RED = settings.COLOR_RED
    ERROR_COLOR_ORANGE = settings.COLOR_ORANGE
    ERRORS_COLORS_CHOICES = (
        (ERROR_COLOR_GREEN, "verde"),
        (ERROR_COLOR_RED, "rojo"),
        (ERROR_COLOR_ORANGE, "naranja"),
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
            "Identificador",
            max_length=255,
            unique=True,
            db_index=True,
            help_text="Identificador único del error",
    )

    description = models.CharField(
            "Descripción",
            max_length=255,
            help_text="Descripción del error",
    )

    operating_system = models.CharField(
            "Sistema Operativo",
            max_length=1,
            choices=OS_CHOICES,
            help_text="Sistema Operativo del ATM",
    )

    color = models.CharField(
            "Color",
            max_length=7,
            choices=ERRORS_COLORS_CHOICES,
            help_text="Color del error",
    )


class AtmEventViewerEvent(models.Model):
    class Meta:
        ordering = ['event_date']

    atm = models.ForeignKey(AtmCase, related_name="event_viewer_errors")

    event_id = models.CharField(max_length=255)

    event_record_id = models.CharField(max_length=255)

    event_date = models.DateTimeField("Fecha del evento")

    context = models.TextField()
