# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('analytics', '0013_auto_20160120_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='atms_number',
            field=models.IntegerField(help_text=b'Cantidad ATMs', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='bank_name',
            field=models.CharField(default='', help_text=b'Nombre del banco', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='email',
            field=models.CharField(default='', help_text=b'Email', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='in_charge',
            field=models.CharField(default='', help_text=b'Nombre del Encargado', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='phone',
            field=models.CharField(default='', help_text=b'Tel\xc3\xa9fono', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='users',
            field=models.ManyToManyField(related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]
