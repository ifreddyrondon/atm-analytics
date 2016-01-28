# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_company_logo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bank',
            options={'ordering': ['position']},
        ),
        migrations.AlterModelOptions(
            name='companyatmlocation',
            options={'ordering': ['position']},
        ),
        migrations.AddField(
            model_name='bank',
            name='position',
            field=models.PositiveSmallIntegerField(null=True, verbose_name=b'Posici\xc3\xb3n'),
        ),
        migrations.AddField(
            model_name='companyatmlocation',
            name='position',
            field=models.PositiveSmallIntegerField(null=True, verbose_name=b'Posici\xc3\xb3n'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='atms_number',
            field=models.IntegerField(help_text=b'Cantidad ATMs', verbose_name=b'ATMs'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='name',
            field=models.CharField(help_text=b'Nombre del Banco', max_length=255, verbose_name=b'Nombre'),
        ),
        migrations.AlterField(
            model_name='company',
            name='email',
            field=models.EmailField(help_text=b'Email', max_length=255, verbose_name=b'Email'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(help_text=b'Nombre de la Empresa', max_length=255, verbose_name=b'Nombre'),
        ),
        migrations.AlterField(
            model_name='company',
            name='phone',
            field=models.CharField(help_text=b'Tel\xc3\xa9fono', max_length=255, verbose_name=b'Tel\xc3\xa9fono'),
        ),
        migrations.AlterField(
            model_name='companyatmlocation',
            name='address',
            field=models.CharField(max_length=255, verbose_name=b'Direci\xc3\xb3n'),
        ),
    ]
