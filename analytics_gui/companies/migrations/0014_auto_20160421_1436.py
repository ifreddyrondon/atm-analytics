# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0013_auto_20160413_0243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xfsformat',
            name='date_pattern',
            field=models.CharField(help_text='This must be a regular expression pattern', max_length=255, verbose_name='Date pattern'),
        ),
        migrations.AlterField(
            model_name='xfsformatevent',
            name='xfs_format',
            field=models.ForeignKey(related_name='format_events', to='companies.XFSFormat'),
        ),
    ]
