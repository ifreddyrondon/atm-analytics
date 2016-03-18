# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0014_auto_20160310_2054'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperatingSystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Operating System')),
            ],
        ),
        migrations.RemoveField(
            model_name='atmerroreventviewer',
            name='operating_system',
        ),
        migrations.RemoveField(
            model_name='atmerrorxfs',
            name='operating_system',
        ),
        migrations.AddField(
            model_name='atmerroreventviewer',
            name='operating_system',
            field=models.ManyToManyField(help_text='ATM Operating System', to='analytics.OperatingSystem'),
        ),
        migrations.AddField(
            model_name='atmerrorxfs',
            name='operating_system',
            field=models.ManyToManyField(help_text='ATM Operating System', to='analytics.OperatingSystem'),
        ),
    ]
