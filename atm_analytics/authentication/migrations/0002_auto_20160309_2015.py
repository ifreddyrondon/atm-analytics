# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userdashboard',
            options={'verbose_name': 'User'},
        ),
        migrations.AlterField(
            model_name='userdashboard',
            name='charge',
            field=models.CharField(max_length=1, verbose_name=b'Cargo', choices=[(b'0', 'analyst'), (b'1', 'manager')]),
        ),
        migrations.AlterField(
            model_name='userdashboard',
            name='company',
            field=models.ForeignKey(related_name='users', verbose_name='Company', to='companies.Company'),
        ),
        migrations.AlterField(
            model_name='userdashboard',
            name='position',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='position'),
        ),
    ]
