# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-07-22 21:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glue2_db', '0011_auto_20180905_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='computingactivity',
            name='LocalOwner',
            field=models.CharField(db_index=True, default='unknown', max_length=40),
        ),
    ]
