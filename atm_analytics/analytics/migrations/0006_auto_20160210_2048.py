# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0005_case_resolution'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtmErrorEventViewer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(help_text=b'Identificador \xc3\xbanico del error', unique=True, max_length=255, verbose_name=b'Identificador', db_index=True)),
                ('description', models.CharField(help_text=b'Descripci\xc3\xb3n del error', max_length=255, verbose_name=b'Descripci\xc3\xb3n')),
                ('operating_system', models.CharField(help_text=b'Sistema Operativo del ATM', max_length=1, verbose_name=b'Sistema Operativo', choices=[(b'0', b'Windows XP'), (b'1', b'Windows 7'), (b'2', b'Windows 8')])),
                ('color', models.CharField(help_text=b'Color del error', max_length=1, verbose_name=b'Color', choices=[(b'0', b'verde'), (b'1', b'rojo'), (b'2', b'naranja')])),
            ],
            options={
                'verbose_name': 'Error EventViewer de ATM',
                'verbose_name_plural': 'Errores EventViewer de ATMs',
            },
        ),
        migrations.RenameModel(
            old_name='AtmError',
            new_name='AtmErrorXFS',
        ),
        migrations.AlterModelOptions(
            name='atmerrorxfs',
            options={'verbose_name': 'Error XFS de ATM', 'verbose_name_plural': 'Errores XFS de ATMs'},
        ),
    ]
