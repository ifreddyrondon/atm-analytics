# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import atm_analytics.companies.models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0011_auto_20160331_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xfsformat',
            name='currency_pattern',
            field=models.CharField(max_length=255, null=True, verbose_name='Currency pattern', blank=True),
        ),
        migrations.AlterField(
            model_name='xfsformat',
            name='date_pattern',
            field=models.CharField(help_text='Select any "date-time" inside the text', max_length=255, verbose_name='Date pattern'),
        ),
        migrations.AlterField(
            model_name='xfsformat',
            name='group_separator',
            field=models.CharField(max_length=255, verbose_name='Group Separator'),
        ),
        migrations.AlterField(
            model_name='xfsformat',
            name='row_separator',
            field=models.CharField(max_length=255, verbose_name='Row Separator'),
        ),
        migrations.AlterField(
            model_name='xfsformat',
            name='total_amount_pattern',
            field=models.CharField(max_length=255, verbose_name='Total amount pattern'),
        ),
        migrations.AlterField(
            model_name='xfsformat',
            name='xfs_sample_file',
            field=models.FileField(upload_to=atm_analytics.companies.models.get_xfs_samples_attachment_path, verbose_name='XFS sample file'),
        ),
    ]
