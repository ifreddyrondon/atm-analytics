# coding=utf-8
import os

from django.db import models


def get_company_logo_attachment_path(instance, filename):
    return os.path.join(
            'company',
            'logo',
            filename
    )


class Company(models.Model):
    logo = models.ImageField(upload_to=get_company_logo_attachment_path, null=True, blank=True)
    name = models.CharField('Nombre', max_length=255, help_text='Nombre de la Empresa')
    email = models.EmailField('Email', max_length=255, help_text='Email')
    phone = models.CharField('Teléfono', max_length=255, help_text='Teléfono')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Compañia"


class Bank(models.Model):
    name = models.CharField('Nombre', max_length=255, help_text='Nombre del Banco')
    atms_number = models.IntegerField('ATMs', help_text='Cantidad ATMs')
    company = models.ForeignKey(Company, related_name="banks")
    position = models.PositiveSmallIntegerField("Posición", null=True)

    class Meta:
        ordering = ['position']
        verbose_name = "Banco"

    def __unicode__(self):
        return self.name


class CompanyAtmLocation(models.Model):
    address = models.CharField('Direción', max_length=255)
    company = models.ForeignKey(Company)
    position = models.PositiveSmallIntegerField("Posición", null=True)

    class Meta:
        ordering = ['position']
        verbose_name = "Direción de ATM"

    def __unicode__(self):
        return self.address
