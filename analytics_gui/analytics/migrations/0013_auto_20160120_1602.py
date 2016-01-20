# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import analytics_gui.analytics.models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0012_atmcase_case'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtmJournal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=analytics_gui.analytics.models.get_atm_journal_virtual_attachment_path)),
            ],
        ),
        migrations.RemoveField(
            model_name='atmcase',
            name='journal_virtual',
        ),
        migrations.AlterField(
            model_name='atmcase',
            name='hardware',
            field=models.CharField(help_text=b'Hardware', max_length=1, choices=[(b'0', b'Diebold'), (b'1', b'Wincor Nixdorf'), (b'2', b'NCR'), (b'3', b'Triton')]),
        ),
        migrations.AlterField(
            model_name='atmcase',
            name='operating_system',
            field=models.CharField(help_text=b'Sistema Operativo', max_length=1, choices=[(b'0', b'Windows XP'), (b'1', b'Windows 7'), (b'2', b'Windows 8')]),
        ),
        migrations.AlterField(
            model_name='atmcase',
            name='software',
            field=models.CharField(help_text=b'Software', max_length=1, choices=[(b'0', b'Agilis'), (b'1', b'APTRA'), (b'2', b'Procash/probase'), (b'3', b'JAM Dynasty'), (b'4', b'Kal'), (b'5', b'Otro XFS')]),
        ),
        migrations.AlterField(
            model_name='case',
            name='analyst_name',
            field=models.CharField(help_text=b'Nombre del analista', max_length=255),
        ),
        migrations.AlterField(
            model_name='case',
            name='name',
            field=models.CharField(help_text=b'Nombre del caso', max_length=255),
        ),
        migrations.AddField(
            model_name='atmjournal',
            name='atm',
            field=models.ForeignKey(related_name='journals', to='analytics.AtmCase'),
        ),
    ]
