# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20160309_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdashboard',
            name='position',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Position'),
        ),
    ]
