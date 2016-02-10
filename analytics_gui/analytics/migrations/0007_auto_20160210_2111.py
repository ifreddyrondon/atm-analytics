# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0006_auto_20160210_2048'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='atmerroreventviewer',
            options={'verbose_name': 'Error de EventViewer', 'verbose_name_plural': 'Errores de EventViewer'},
        ),
        migrations.AlterModelOptions(
            name='atmerrorxfs',
            options={'verbose_name': 'Error XFS', 'verbose_name_plural': 'Errores XFS'},
        ),
        migrations.AlterField(
            model_name='atmerroreventviewer',
            name='color',
            field=models.CharField(help_text=b'Color del error', max_length=7, verbose_name=b'Color', choices=[(b'#008000', b'verde'), (b'#FF0000', b'rojo'), (b'#FF9300', b'naranja')]),
        ),
    ]
