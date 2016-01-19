# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import analytics_gui.analytics.models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0009_atmcase_other_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='atmcase',
            name='atm_location',
            field=models.CharField(default='', help_text=b'Localizaci\xc3\xb3n del ATM', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='case',
            name='description',
            field=models.TextField(help_text=b'Breve descripci\xc3\xb3n extra del caso', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='case',
            name='missing_amount',
            field=models.DecimalField(default=1, help_text=b'Monto faltante estimado', max_digits=19, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='atmcase',
            name='journal_virtual',
            field=models.FileField(help_text=b'Seleccionar Journal Virtual', upload_to=analytics_gui.analytics.models.get_atm_journal_virtual_attachment_path),
        ),
        migrations.AlterField(
            model_name='atmcase',
            name='other_log',
            field=models.FileField(help_text=b'\xc2\xbfOtro tipo de log?', null=True, upload_to=analytics_gui.analytics.models.get_atm_other_log_attachment_path, blank=True),
        ),
    ]
