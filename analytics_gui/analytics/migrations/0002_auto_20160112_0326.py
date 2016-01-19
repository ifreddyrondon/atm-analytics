# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Nombre de la Empresa', max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='case',
            name='company',
            field=models.ForeignKey(default=1, to='analytics.Company', help_text=b'Empresa'),
            preserve_default=False,
        ),
    ]
