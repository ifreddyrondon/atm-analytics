# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import analytics_gui.analytics.models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0004_auto_20160113_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='atmcase',
            name='errors_manual',
            field=models.FileField(null=True, upload_to=analytics_gui.analytics.models.get_atm_errors_manual_attachment_path, blank=True),
        ),
    ]
