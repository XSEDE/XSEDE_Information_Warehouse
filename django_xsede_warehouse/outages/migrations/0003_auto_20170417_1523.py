# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-17 15:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outages', '0002_outages_outagetype'),
    ]

    operations = [
        migrations.AddField(
            model_name='outages',
            name='ID',
            field=models.CharField(default='1234:asdfasdfsa', max_length=128, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='outages',
            name='OutageID',
            field=models.IntegerField(),
        ),
    ]
