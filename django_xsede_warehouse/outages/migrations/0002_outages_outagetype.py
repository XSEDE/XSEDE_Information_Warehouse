# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-26 12:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='outages',
            name='OutageType',
            field=models.CharField(default='Full', max_length=16),
            preserve_default=False,
        ),
    ]
