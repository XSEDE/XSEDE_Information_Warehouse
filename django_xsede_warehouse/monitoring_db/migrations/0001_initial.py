# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('ID', models.CharField(max_length=120, serialize=False, primary_key=True)),
                ('ResourceID', models.CharField(max_length=40, db_index=True)),
                ('Name', models.CharField(max_length=128, null=True)),
                ('CreationTime', models.DateTimeField()),
                ('EntityJSON', jsonfield.fields.JSONField(default=dict)),
                ('Source', models.CharField(max_length=16)),
                ('Result', models.CharField(max_length=16)),
                ('ErrorMessage', models.CharField(max_length=512, null=True)),
                ('IsSoftware', models.BooleanField(default=False)),
                ('IsService', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
                'db_name': 'glue2',
            },
        ),
    ]
