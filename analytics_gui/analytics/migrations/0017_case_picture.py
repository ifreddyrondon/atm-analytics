# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import analytics_gui.analytics.models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0016_auto_20160127_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='picture',
            field=models.ImageField(null=True, upload_to=analytics_gui.analytics.models.get_case_picture_path, blank=True),
        ),
    ]
