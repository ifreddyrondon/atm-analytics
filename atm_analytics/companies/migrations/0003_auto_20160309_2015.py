# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_atmrepositionevent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bank',
            options={'ordering': ['position'], 'verbose_name': 'Bank'},
        ),
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'Company'},
        ),
        migrations.AlterModelOptions(
            name='companyatmlocation',
            options={'ordering': ['position'], 'verbose_name': 'ATM address'},
        ),
        migrations.AlterField(
            model_name='bank',
            name='atms_number',
            field=models.IntegerField(help_text='Number of ATMs', verbose_name=b'ATMs'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='name',
            field=models.CharField(help_text='Bank name', max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='position',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Position'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(help_text='Company name', max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='company',
            name='phone',
            field=models.CharField(help_text='Phone number', max_length=255, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='companyatmlocation',
            name='address',
            field=models.CharField(max_length=255, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='companyatmlocation',
            name='position',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Position'),
        ),
    ]
