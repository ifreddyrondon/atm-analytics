# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(help_text=b'N\xc3\xbamero de caso', db_index=True)),
                ('name', models.CharField(help_text=b'Nombre del analista', max_length=255)),
                ('analyst_name', models.CharField(help_text=b'Analista', max_length=255)),
            ],
        ),
    ]
