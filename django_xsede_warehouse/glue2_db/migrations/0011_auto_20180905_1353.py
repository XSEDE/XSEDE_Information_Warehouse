# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-09-05 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glue2_db', '0010_auto_20180524_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationenvironment',
            name='AppVersion',
            field=models.CharField(default='none', max_length=64),
        ),
    ]
