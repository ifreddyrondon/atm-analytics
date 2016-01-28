# coding=utf-8
import os

from django.contrib.auth.models import User
from django.db import models


def get_company_logo_attachment_path(instance, filename):
    return os.path.join(
            'company',
            'logo',
            filename
    )


# Create your models here.
class Company(models.Model):
    logo = models.ImageField(upload_to=get_company_logo_attachment_path, null=True, blank=True)
    name = models.CharField('Nombre', max_length=255, help_text='Nombre de la Empresa')
    email = models.EmailField('Email', max_length=255, help_text='Email')
    phone = models.CharField('Teléfono', max_length=255, help_text='Teléfono')
    in_charge = models.OneToOneField(User, related_name='manager')
    users = models.ForeignKey(User, related_name='users')

    def __unicode__(self):
        return self.name


class Bank(models.Model):
    name = models.CharField('Nombre', max_length=255, help_text='Nombre del Banco')
    atms_number = models.IntegerField('ATMs', help_text='Cantidad ATMs')
    company = models.ForeignKey(Company, related_name="banks")
    position = models.PositiveSmallIntegerField("Posición", null=True)

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        return self.name


class CompanyAtmLocation(models.Model):
    address = models.CharField('Direción', max_length=255)
    company = models.ForeignKey(Company)
    position = models.PositiveSmallIntegerField("Posición", null=True)

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        return self.address
