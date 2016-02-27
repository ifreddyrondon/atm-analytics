# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0010_atmeventviewerevent_atm'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='atmeventviewerevent',
            options={'ordering': ['event_date']},
        ),
        migrations.RemoveField(
            model_name='atmeventviewerevent',
            name='record_id',
        ),
        migrations.AddField(
            model_name='atmeventviewerevent',
            name='event_id',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='atmeventviewerevent',
            name='event_record_id',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
