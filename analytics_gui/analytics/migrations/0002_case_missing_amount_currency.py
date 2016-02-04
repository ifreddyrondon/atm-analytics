# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='missing_amount_currency',
            field=models.CharField(default='0', help_text=b'Divisa', max_length=1, choices=[(b'0', b'dolar US'), (b'1', b'euro')]),
            preserve_default=False,
        ),
    ]
