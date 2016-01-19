# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import analytics_gui.analytics.models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0008_auto_20160114_0026'),
    ]

    operations = [
        migrations.AddField(
            model_name='atmcase',
            name='other_log',
            field=models.FileField(null=True, upload_to=analytics_gui.analytics.models.get_atm_other_log_attachment_path, blank=True),
        ),
    ]
