# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0008_xfsformat_content_xfs_file_sample'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='xfsformat',
            name='content_xfs_file_sample',
        ),
    ]
