# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-17 01:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing_status', '0002_processingerror_reference1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processingrecord',
            name='ProcessingEnd',
            field=models.DateTimeField(null=True),
        ),
    ]
