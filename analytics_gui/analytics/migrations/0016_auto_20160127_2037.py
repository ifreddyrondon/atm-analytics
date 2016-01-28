# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20160127_2037'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('analytics', '0015_auto_20160127_1822'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='users',
        ),
        migrations.RemoveField(
            model_name='companyatmlocation',
            name='company',
        ),
        migrations.RemoveField(
            model_name='case',
            name='analyst_name',
        ),
        migrations.RemoveField(
            model_name='case',
            name='company',
        ),
        migrations.AddField(
            model_name='case',
            name='analyst',
            field=models.ForeignKey(related_name='analyst_cases', default=0, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='case',
            name='bank',
            field=models.ForeignKey(related_name='bank_cases', default=0, to='authentication.Bank'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='atmcase',
            name='atm_location',
            field=models.ManyToManyField(help_text=b'Localizaci\xc3\xb3n del ATM', to='authentication.CompanyAtmLocation'),
        ),
        migrations.DeleteModel(
            name='Company',
        ),
        migrations.DeleteModel(
            name='CompanyAtmLocation',
        ),
    ]
