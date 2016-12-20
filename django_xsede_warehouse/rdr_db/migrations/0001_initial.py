# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RDRResource',
            fields=[
                ('rdr_resource_id', models.IntegerField(serialize=False, primary_key=True)),
                ('rdr_type', models.CharField(max_length=16)),
                ('info_resourceid', models.CharField(max_length=40, db_index=True)),
                ('info_siteid', models.CharField(max_length=40, db_index=True)),
                ('resource_descriptive_name', models.CharField(max_length=120)),
                ('resource_description', models.CharField(max_length=2000, null=True)),
                ('resource_status', jsonfield.fields.JSONField(default=dict)),
                ('current_statuses', models.CharField(max_length=64)),
                ('parent_resource', models.IntegerField(null=True)),
                ('recommended_use', models.CharField(max_length=2000, null=True)),
                ('access_description', models.CharField(max_length=2000, null=True)),
                ('other_attributes', jsonfield.fields.JSONField(default=dict)),
                ('updated_at', models.DateTimeField(null=True)),
            ],
            options={
                'db_name': 'xcsr',
            },
        ),
    ]
