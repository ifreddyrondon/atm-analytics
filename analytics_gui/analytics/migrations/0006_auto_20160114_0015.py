# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import analytics_gui.analytics.models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0005_atmcase_errors_manual'),
    ]

    operations = [
        migrations.AddField(
            model_name='atmcase',
            name='cash_replacement_schedule',
            field=models.FileField(null=True, upload_to=analytics_gui.analytics.models.get_atm_cash_replacement_schedule_attachment_path, blank=True),
        ),
        migrations.AddField(
            model_name='atmcase',
            name='microsoft_event_viewer',
            field=models.FileField(null=True, upload_to=analytics_gui.analytics.models.get_atm_microsoft_event_viewer_attachment_path, blank=True),
        ),
    ]
