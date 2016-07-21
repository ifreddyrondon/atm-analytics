# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import atm_analytics.companies.models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0010_xfsformat_xfs_sample_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xfsformat',
            name='xfs_sample_file',
            field=models.FileField(default=1, upload_to=atm_analytics.companies.models.get_xfs_samples_attachment_path),
            preserve_default=False,
        ),
    ]
