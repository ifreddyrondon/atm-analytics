# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import analytics_gui.authentication.models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20160127_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='logo',
            field=models.ImageField(null=True, upload_to=analytics_gui.authentication.models.get_company_logo_attachment_path, blank=True),
        ),
    ]
