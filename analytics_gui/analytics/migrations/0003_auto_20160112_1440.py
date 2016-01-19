# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_auto_20160112_0326'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='priority',
            field=models.CharField(default='0', help_text=b'Importancia del caso', max_length=1, choices=[(b'0', b'bajo'), (b'1', b'medio'), (b'2', b'alto')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='case',
            name='status',
            field=models.CharField(default='0', help_text=b'Estado del caso', max_length=1, choices=[(b'0', b'abierto'), (b'1', b'cerrado')]),
            preserve_default=False,
        ),
    ]
