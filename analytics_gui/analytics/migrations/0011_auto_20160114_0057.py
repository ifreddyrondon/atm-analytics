# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0010_auto_20160114_0048'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyAtmLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=255)),
                ('company', models.ForeignKey(to='analytics.Company')),
            ],
        ),
        migrations.RemoveField(
            model_name='atmcase',
            name='atm_location',
        ),
        migrations.AddField(
            model_name='atmcase',
            name='atm_location',
            field=models.ManyToManyField(help_text=b'Localizaci\xc3\xb3n del ATM', to='analytics.CompanyAtmLocation'),
        ),
    ]
