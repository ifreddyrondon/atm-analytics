# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0018_auto_20160128_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='analyst',
            field=models.ForeignKey(related_name='analyst_cases', to='authentication.UserDashboard'),
        ),
    ]
