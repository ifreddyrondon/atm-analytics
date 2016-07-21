# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0012_auto_20160401_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xfsformatevent',
            name='type',
            field=models.CharField(help_text='Type of event', max_length=1, choices=[(b'0', b'Critical error'), (b'1', b'Important error'), (b'2', b'No error')]),
        ),
    ]
