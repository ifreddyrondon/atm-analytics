# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0014_auto_20160421_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='xfsformat',
            name='is_day_first',
            field=models.BooleanField(default=True, verbose_name='Is day first?'),
        ),
    ]
