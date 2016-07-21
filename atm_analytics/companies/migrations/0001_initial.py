# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import atm_analytics.companies.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Nombre del Banco', max_length=255, verbose_name=b'Nombre')),
                ('atms_number', models.IntegerField(help_text=b'Cantidad ATMs', verbose_name=b'ATMs')),
                ('position', models.PositiveSmallIntegerField(null=True, verbose_name=b'Posici\xc3\xb3n')),
            ],
            options={
                'ordering': ['position'],
                'verbose_name': 'Banco',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('logo', models.ImageField(null=True, upload_to=atm_analytics.companies.models.get_company_logo_attachment_path, blank=True)),
                ('name', models.CharField(help_text=b'Nombre de la Empresa', max_length=255, verbose_name=b'Nombre')),
                ('email', models.EmailField(help_text=b'Email', max_length=255, verbose_name=b'Email')),
                ('phone', models.CharField(help_text=b'Tel\xc3\xa9fono', max_length=255, verbose_name=b'Tel\xc3\xa9fono')),
            ],
            options={
                'verbose_name': 'Compa\xf1ia',
            },
        ),
        migrations.CreateModel(
            name='CompanyAtmLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=255, verbose_name=b'Direci\xc3\xb3n')),
                ('position', models.PositiveSmallIntegerField(null=True, verbose_name=b'Posici\xc3\xb3n')),
                ('company', models.ForeignKey(to='companies.Company')),
            ],
            options={
                'ordering': ['position'],
                'verbose_name': 'Direci\xf3n de ATM',
            },
        ),
        migrations.AddField(
            model_name='bank',
            name='company',
            field=models.ForeignKey(related_name='banks', to='companies.Company'),
        ),
    ]
