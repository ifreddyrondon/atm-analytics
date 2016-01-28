# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0002_delete_case'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Nombre del Banco', max_length=255)),
                ('atms_number', models.IntegerField(help_text=b'Cantidad ATMs')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Nombre de la Empresa', max_length=255)),
                ('email', models.EmailField(help_text=b'Email', max_length=255)),
                ('phone', models.CharField(help_text=b'Tel\xc3\xa9fono', max_length=255)),
                ('in_charge', models.OneToOneField(related_name='manager', to=settings.AUTH_USER_MODEL)),
                ('users', models.ForeignKey(related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyAtmLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=255)),
                ('company', models.ForeignKey(to='authentication.Company')),
            ],
        ),
        migrations.AddField(
            model_name='bank',
            name='company',
            field=models.ForeignKey(related_name='banks', to='authentication.Company'),
        ),
    ]
