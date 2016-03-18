# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management import call_command
from django.db import migrations


def load_fixture(apps, schema_editor):
    call_command('loaddata', 'operating_systems.json')


class Migration(migrations.Migration):
    dependencies = [
        ('analytics', '0015_auto_20160318_2045'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]
