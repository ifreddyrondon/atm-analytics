# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import analytics_gui.analytics.models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0007_auto_20160114_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atmcase',
            name='journal_virtual',
            field=models.FileField(default='', upload_to=analytics_gui.analytics.models.get_atm_journal_virtual_attachment_path),
            preserve_default=False,
        ),
    ]
