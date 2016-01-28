# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_auto_20160128_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='users',
            field=models.ManyToManyField(related_name='users', null=True, verbose_name=b'Usuarios', to='authentication.UserDashboard', blank=True),
        ),
    ]
