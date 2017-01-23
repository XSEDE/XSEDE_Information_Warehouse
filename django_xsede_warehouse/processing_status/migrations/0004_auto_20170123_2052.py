# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-23 20:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing_status', '0003_auto_20170117_0140'),
    ]

    operations = [
        migrations.RenameField(
            model_name='processingerror',
            old_name='ProcessingApp',
            new_name='ProcessingApplication',
        ),
        migrations.RenameField(
            model_name='processingrecord',
            old_name='ProcessingApp',
            new_name='ProcessingApplication',
        ),
        migrations.AddField(
            model_name='processingerror',
            name='ProcessingFunction',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='processingrecord',
            name='ProcessingFunction',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
