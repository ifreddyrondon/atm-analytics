# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0005_auto_20160127_2116'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDashboard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.CharField(max_length=1, choices=[(b'0', b'analista'), (b'1', b'admin')])),
                ('user', models.OneToOneField(related_name='dash_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='company',
            name='in_charge',
            field=models.OneToOneField(related_name='manager', to='authentication.UserDashboard'),
        ),
        migrations.AlterField(
            model_name='company',
            name='users',
            field=models.ForeignKey(related_name='users', to='authentication.UserDashboard'),
        ),
    ]
