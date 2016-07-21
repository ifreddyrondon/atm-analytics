# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0007_auto_20160331_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='xfsformat',
            name='content_xfs_file_sample',
            field=models.TextField(null=True, blank=True),
        ),
    ]
