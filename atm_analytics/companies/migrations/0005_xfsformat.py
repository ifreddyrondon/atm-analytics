# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0004_auto_20160309_2018'),
    ]

    operations = [
        migrations.CreateModel(
            name='XFSFormat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hardware', models.CharField(help_text='Hardware', max_length=1, choices=[(b'0', b'Diebold'), (b'1', b'Wincor Nixdorf'), (b'2', b'NCR'), (b'3', b'Triton')])),
                ('software', models.CharField(help_text='Software', max_length=1, choices=[(b'0', b'Agilis'), (b'1', b'APTRA'), (b'2', b'Procash/probase'), (b'3', b'JAM Dynasty'), (b'4', b'Kal'), (b'5', 'Other XFS')])),
                ('position', models.PositiveSmallIntegerField(null=True, verbose_name='Position')),
                ('company', models.ForeignKey(to='companies.Company')),
            ],
            options={
                'ordering': ['position'],
                'verbose_name': 'XFS Formats',
            },
        ),
    ]
