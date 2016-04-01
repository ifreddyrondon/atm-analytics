# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0005_xfsformat'),
    ]

    operations = [
        migrations.AddField(
            model_name='xfsformat',
            name='currency_pattern',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='xfsformat',
            name='date_pattern',
            field=models.CharField(help_text='Select any "date-time" inside the text', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='xfsformat',
            name='group_separator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='xfsformat',
            name='row_separator',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='xfsformat',
            name='total_amount_pattern',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
