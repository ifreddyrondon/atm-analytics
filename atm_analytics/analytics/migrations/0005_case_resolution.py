# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0004_auto_20160208_0107'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='resolution',
            field=models.TextField(null=True, blank=True),
        ),
    ]
