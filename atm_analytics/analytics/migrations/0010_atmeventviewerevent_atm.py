# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0009_atmeventviewerevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='atmeventviewerevent',
            name='atm',
            field=models.ForeignKey(related_name='event_viewer_errors', default=1, to='analytics.AtmCase'),
            preserve_default=False,
        ),
    ]
