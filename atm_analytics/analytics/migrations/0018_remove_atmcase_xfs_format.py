# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0017_atmcase_xfs_format'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atmcase',
            name='xfs_format',
        ),
    ]
