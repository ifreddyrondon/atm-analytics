# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0013_auto_20160413_0243'),
        ('analytics', '0016_auto_20160318_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='atmcase',
            name='xfs_format',
            field=models.ForeignKey(blank=True, to='companies.XFSFormat', null=True),
        ),
    ]
