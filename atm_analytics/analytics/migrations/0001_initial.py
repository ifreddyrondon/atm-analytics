# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import atm_analytics.analytics.models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtmCase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hardware', models.CharField(help_text=b'Hardware', max_length=1, choices=[(b'0', b'Diebold'), (b'1', b'Wincor Nixdorf'), (b'2', b'NCR'), (b'3', b'Triton')])),
                ('software', models.CharField(help_text=b'Software', max_length=1, choices=[(b'0', b'Agilis'), (b'1', b'APTRA'), (b'2', b'Procash/probase'), (b'3', b'JAM Dynasty'), (b'4', b'Kal'), (b'5', b'Otro XFS')])),
                ('operating_system', models.CharField(help_text=b'Sistema Operativo', max_length=1, choices=[(b'0', b'Windows XP'), (b'1', b'Windows 7'), (b'2', b'Windows 8')])),
                ('errors_manual', models.FileField(null=True, upload_to=atm_analytics.analytics.models.get_atm_errors_manual_attachment_path, blank=True)),
                ('microsoft_event_viewer', models.FileField(null=True, upload_to=atm_analytics.analytics.models.get_atm_microsoft_event_viewer_attachment_path, blank=True)),
                ('cash_replacement_schedule', models.FileField(null=True, upload_to="media", blank=True)),
                ('person_name_journal_virtual', models.CharField(help_text=b'Nombre de la persona que le facilito el Journal virtual', max_length=255)),
                ('other_log', models.FileField(help_text=b'\xc2\xbfOtro tipo de log?', null=True, upload_to=atm_analytics.analytics.models.get_atm_other_log_attachment_path, blank=True)),
                ('atm_location', models.ManyToManyField(help_text=b'Localizaci\xc3\xb3n del ATM', related_name='locations', to='companies.CompanyAtmLocation')),
            ],
            options={
                'verbose_name': 'ATM',
                'verbose_name_plural': 'ATMs',
            },
        ),
        migrations.CreateModel(
            name='AtmError',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(help_text=b'Identificador \xc3\xbanico del error', unique=True, max_length=255, verbose_name=b'Identificador', db_index=True)),
                ('description', models.CharField(help_text=b'Descripci\xc3\xb3n del error', max_length=255, verbose_name=b'Descripci\xc3\xb3n')),
                ('hardware', models.CharField(help_text=b'Hardware del ATM', max_length=1, verbose_name=b'Hardware', choices=[(b'0', b'Diebold'), (b'1', b'Wincor Nixdorf'), (b'2', b'NCR'), (b'3', b'Triton')])),
                ('software', models.CharField(help_text=b'Software del ATM', max_length=1, verbose_name=b'Software', choices=[(b'0', b'Agilis'), (b'1', b'APTRA'), (b'2', b'Procash/probase'), (b'3', b'JAM Dynasty'), (b'4', b'Kal'), (b'5', b'Otro XFS')])),
                ('operating_system', models.CharField(help_text=b'Sistema Operativo del ATM', max_length=1, verbose_name=b'Sistema Operativo', choices=[(b'0', b'Windows XP'), (b'1', b'Windows 7'), (b'2', b'Windows 8')])),
                ('fault', models.CharField(help_text=b'\xc2\xbfQui\xc3\xa9n tiene la culpa?', max_length=1, verbose_name=b'Culpa', choices=[(b'0', b'usuario'), (b'1', b'banco'), (b'1', b'transvalores'), (b'3', b'anonimo')])),
                ('color', models.CharField(help_text=b'Color del error', max_length=1, verbose_name=b'Color', choices=[(b'0', b'verde'), (b'1', b'rojo'), (b'2', b'naranja')])),
            ],
            options={
                'verbose_name': 'Error de ATM',
                'verbose_name_plural': 'Errores de ATMs',
            },
        ),
        migrations.CreateModel(
            name='AtmJournal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=atm_analytics.analytics.models.get_atm_journal_virtual_attachment_path)),
                ('atm', models.ForeignKey(related_name='journals', to='analytics.AtmCase')),
            ],
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(help_text=b'N\xc3\xbamero de caso', db_index=True)),
                ('picture', models.ImageField(null=True, upload_to=atm_analytics.analytics.models.get_case_picture_path, blank=True)),
                ('name', models.CharField(help_text=b'Nombre del caso', max_length=255)),
                ('priority', models.CharField(help_text=b'Importancia del caso', max_length=1, choices=[(b'0', b'bajo'), (b'1', b'medio'), (b'2', b'alto')])),
                ('status', models.CharField(default=b'0', help_text=b'Estado del caso', max_length=1, choices=[(b'0', b'abierto'), (b'1', b'cerrado')])),
                ('created_date', models.DateField(help_text=b'Fecha de creaci\xc3\xb3n del caso', null=True, blank=True)),
                ('missing_amount', models.DecimalField(help_text=b'Monto faltante estimado', max_digits=19, decimal_places=2)),
                ('description', models.TextField(help_text=b'Breve descripci\xc3\xb3n extra del caso', null=True, blank=True)),
                ('analyst', models.ForeignKey(related_name='analyst_cases', to='authentication.UserDashboard')),
                ('bank', models.ForeignKey(related_name='bank_cases', to='companies.Bank', help_text=b'Banco')),
            ],
            options={
                'verbose_name': 'Caso',
            },
        ),
        migrations.AddField(
            model_name='atmcase',
            name='case',
            field=models.ForeignKey(related_name='atms', to='analytics.Case'),
        ),
    ]
