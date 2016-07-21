# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0008_auto_20160222_2117'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtmEventViewerEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('record_id', models.CharField(help_text=b'Identificador \xc3\xbanico del error', max_length=255, verbose_name=b'Identificador')),
                ('event_date', models.DateTimeField(verbose_name=b'Fecha del evento')),
                ('context', models.TextField()),
            ],
        ),
    ]
