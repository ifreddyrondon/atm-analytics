# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_auto_20160112_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtmCase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hardware', models.CharField(max_length=1, choices=[(b'0', b'Diebold'), (b'1', b'Wincor Nixdorf'), (b'2', b'NCR'), (b'3', b'Triton')])),
                ('software', models.CharField(max_length=1, choices=[(b'0', b'Agilis'), (b'1', b'APTRA'), (b'2', b'Procash/probase'), (b'3', b'JAM Dynasty'), (b'4', b'Kal'), (b'5', b'Otro XFS')])),
                ('operating_system', models.CharField(max_length=1, choices=[(b'0', b'Windows XP'), (b'1', b'Windows 7'), (b'2', b'Windows 8')])),
            ],
        ),
        migrations.AddField(
            model_name='case',
            name='created_date',
            field=models.DateField(help_text=b'Fecha de creaci\xc3\xb3n del caso', null=True, blank=True),
        ),
    ]
