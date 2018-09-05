# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
#import jsonfield.fields
from django.contrib.postgres.fields import JSONField


class Migration(migrations.Migration):

    replaces = [('rdr_db', '0001_initial'), ('rdr_db', '0002_auto_20160524_0104'), ('rdr_db', '0003_auto_20160524_0115')]

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
                ('resource_description', models.CharField(max_length=4000, null=True)),
                ('resource_status', JSONField(default=dict)),
                ('current_statuses', models.CharField(max_length=64)),
                ('parent_resource', models.IntegerField(null=True)),
                ('recommended_use', models.CharField(max_length=4000, null=True)),
                ('access_description', models.CharField(max_length=4000, null=True)),
                ('other_attributes', JSONField(default=dict)),
                ('updated_at', models.DateTimeField(null=True)),
            ],
            options={
                'db_name': 'xcsr',
            },
        ),
    ]
