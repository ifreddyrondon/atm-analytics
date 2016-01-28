# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_auto_20160128_1835'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name_plural': 'Companies'},
        ),
        migrations.AlterModelOptions(
            name='userdashboard',
            options={'verbose_name': 'User'},
        ),
        migrations.AlterField(
            model_name='company',
            name='in_charge',
            field=models.OneToOneField(related_name='manager', verbose_name=b'Manager', to='authentication.UserDashboard'),
        ),
        migrations.RemoveField(
            model_name='company',
            name='users',
        ),
        migrations.AddField(
            model_name='company',
            name='users',
            field=models.ManyToManyField(related_name='users', verbose_name=b'Usuarios', to='authentication.UserDashboard'),
        ),
    ]
