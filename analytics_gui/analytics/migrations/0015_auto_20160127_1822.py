# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0014_auto_20160127_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='email',
            field=models.EmailField(help_text=b'Email', max_length=255),
        ),
        migrations.AlterField(
            model_name='company',
            name='users',
            field=models.ManyToManyField(related_name='company_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
