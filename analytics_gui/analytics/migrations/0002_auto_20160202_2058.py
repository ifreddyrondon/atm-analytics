# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtmError',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(unique=True, max_length=255, verbose_name=b'Identificador', db_index=True)),
                ('description', models.CharField(max_length=255, verbose_name=b'Descripci\xc3\xb3n')),
                ('fault', models.CharField(help_text=b'\xc2\xbfQui\xc3\xa9n tiene la culpa?', max_length=1, verbose_name=b'Culpa', choices=[(b'0', b'usuario'), (b'1', b'banco')])),
                ('color', models.CharField(help_text=b'Color del error', max_length=1, verbose_name=b'Color', choices=[(b'0', b'verde'), (b'1', b'rojo')])),
            ],
            options={
                'verbose_name': 'Error de ATM',
                'verbose_name_plural': 'Errores de ATMs',
            },
        ),
        migrations.AlterModelOptions(
            name='atmcase',
            options={'verbose_name': 'ATM', 'verbose_name_plural': 'ATMs'},
        ),
        migrations.AlterModelOptions(
            name='case',
            options={'verbose_name': 'Caso'},
        ),
    ]
