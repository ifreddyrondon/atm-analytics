# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import analytics_gui.companies.models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0009_remove_xfsformat_content_xfs_file_sample'),
    ]

    operations = [
        migrations.AddField(
            model_name='xfsformat',
            name='xfs_sample_file',
            field=models.FileField(null=True, upload_to=analytics_gui.companies.models.get_xfs_samples_attachment_path, blank=True),
        ),
    ]
