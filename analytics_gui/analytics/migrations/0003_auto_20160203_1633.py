# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_auto_20160202_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='atmerror',
            name='hardware',
            field=models.CharField(default=0, help_text=b'Hardware', max_length=1, choices=[(b'0', b'Diebold'), (b'1', b'Wincor Nixdorf'), (b'2', b'NCR'), (b'3', b'Triton')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='atmerror',
            name='operating_system',
            field=models.CharField(default='0', help_text=b'Sistema Operativo', max_length=1, choices=[(b'0', b'Windows XP'), (b'1', b'Windows 7'), (b'2', b'Windows 8')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='atmerror',
            name='software',
            field=models.CharField(default='0', help_text=b'Software', max_length=1, choices=[(b'0', b'Agilis'), (b'1', b'APTRA'), (b'2', b'Procash/probase'), (b'3', b'JAM Dynasty'), (b'4', b'Kal'), (b'5', b'Otro XFS')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='atmerror',
            name='color',
            field=models.CharField(help_text=b'Color del error', max_length=1, verbose_name=b'Color', choices=[(b'0', b'verde'), (b'1', b'rojo'), (b'2', b'naranja')]),
        ),
        migrations.AlterField(
            model_name='atmerror',
            name='description',
            field=models.CharField(help_text=b'Descripci\xc3\xb3n del error', max_length=255, verbose_name=b'Descripci\xc3\xb3n'),
        ),
        migrations.AlterField(
            model_name='atmerror',
            name='fault',
            field=models.CharField(help_text=b'\xc2\xbfQui\xc3\xa9n tiene la culpa?', max_length=1, verbose_name=b'Culpa', choices=[(b'0', b'usuario'), (b'1', b'banco'), (b'1', b'transvalores'), (b'3', b'anonimo')]),
        ),
        migrations.AlterField(
            model_name='atmerror',
            name='identifier',
            field=models.CharField(help_text=b'Identificador \xc3\xbanico del error', unique=True, max_length=255, verbose_name=b'Identificador', db_index=True),
        ),
    ]
