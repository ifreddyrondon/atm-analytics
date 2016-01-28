# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0017_case_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='bank',
            field=models.ForeignKey(related_name='bank_cases', to='authentication.Bank', help_text=b'Banco'),
        ),
    ]
