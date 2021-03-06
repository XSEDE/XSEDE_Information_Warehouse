# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-02 00:29
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glue2_db', '0007_auto_20171101_1010'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComputingQueue',
            fields=[
                ('ID', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=128, null=True)),
                ('CreationTime', models.DateTimeField()),
                ('Validity', models.DurationField(null=True)),
                ('EntityJSON', django.contrib.postgres.fields.jsonb.JSONField()),
                ('ResourceID', models.CharField(db_index=True, max_length=40)),
            ],
            options={
                'abstract': False,
                'db_name': 'glue2',
            },
        ),
    ]
