# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0011_auto_20160226_2240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atmcase',
            name='cash_replacement_schedule',
        ),
    ]
