# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0006_auto_20160330_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='XFSFormatEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pattern', models.CharField(max_length=255)),
                ('type', models.CharField(help_text='Type of event', max_length=1, choices=[(b'0', b'Critical erros'), (b'1', b'Important error'), (b'2', b'No error')])),
            ],
        ),
        migrations.AlterField(
            model_name='xfsformat',
            name='group_separator',
            field=models.CharField(max_length=255, null=True, verbose_name='Group Separator', blank=True),
        ),
        migrations.AddField(
            model_name='xfsformatevent',
            name='xfs_format',
            field=models.ForeignKey(to='companies.XFSFormat'),
        ),
    ]
