# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0007_auto_20160210_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atmerrorxfs',
            name='color',
            field=models.CharField(help_text=b'Color del error', max_length=1, verbose_name=b'Color', choices=[(b'#008000', b'verde'), (b'#FF0000', b'rojo'), (b'#FF9300', b'naranja')]),
        ),
    ]
