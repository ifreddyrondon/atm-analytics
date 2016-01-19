# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import analytics_gui.analytics.models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0006_auto_20160114_0015'),
    ]

    operations = [
        migrations.AddField(
            model_name='atmcase',
            name='journal_virtual',
            field=models.FileField(null=True, upload_to=analytics_gui.analytics.models.get_atm_journal_virtual_attachment_path, blank=True),
        ),
        migrations.AddField(
            model_name='atmcase',
            name='person_name_journal_virtual',
            field=models.CharField(default='', help_text=b'Nombre de la persona que le facilito el Journal virtual', max_length=255),
            preserve_default=False,
        ),
    ]
