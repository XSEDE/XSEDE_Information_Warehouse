# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-02 20:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource_cat', '0002_auto_20180905_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='LocalID',
            field=models.CharField(db_index=True, max_length=200, null=True),
        ),
    ]
