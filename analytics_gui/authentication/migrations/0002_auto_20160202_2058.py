# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdashboard',
            name='position',
            field=models.CharField(max_length=1, choices=[(b'0', b'analista'), (b'1', b'manager')]),
        ),
    ]
