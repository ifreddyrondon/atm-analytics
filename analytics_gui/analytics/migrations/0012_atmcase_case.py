# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0011_auto_20160114_0057'),
    ]

    operations = [
        migrations.AddField(
            model_name='atmcase',
            name='case',
            field=models.ForeignKey(related_name='atms', default=0, to='analytics.Case'),
            preserve_default=False,
        ),
    ]
