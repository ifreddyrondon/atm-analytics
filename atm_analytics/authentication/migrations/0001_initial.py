# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDashboard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('charge', models.CharField(max_length=1, verbose_name=b'Cargo', choices=[(b'0', b'analista'), (b'1', b'manager')])),
                ('position', models.PositiveSmallIntegerField(null=True, verbose_name=b'Posici\xc3\xb3n')),
                ('company', models.ForeignKey(related_name='users', verbose_name=b'Compa\xc3\xb1ia', to='companies.Company')),
                ('user', models.OneToOneField(related_name='dash_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Usuario',
            },
        ),
    ]
