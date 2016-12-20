# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractService',
            fields=[
                ('ID', models.CharField(max_length=120, serialize=False, primary_key=True)),
                ('ResourceID', models.CharField(max_length=40, db_index=True)),
                ('Name', models.CharField(max_length=96)),
                ('CreationTime', models.DateTimeField()),
                ('EntityJSON', jsonfield.fields.JSONField(default=dict)),
                ('ServiceType', models.CharField(max_length=16)),
            ],
            options={
                'abstract': False,
                'db_name': 'glue2',
            },
        ),
        migrations.CreateModel(
            name='ApplicationEnvironment',
            fields=[
                ('ID', models.CharField(max_length=120, serialize=False, primary_key=True)),
                ('ResourceID', models.CharField(max_length=40, db_index=True)),
                ('Name', models.CharField(max_length=96)),
                ('CreationTime', models.DateTimeField()),
                ('EntityJSON', jsonfield.fields.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
                'db_name': 'glue2',
            },
        ),
        migrations.CreateModel(
            name='ApplicationHandle',
            fields=[
                ('ID', models.CharField(max_length=120, serialize=False, primary_key=True)),
                ('ResourceID', models.CharField(max_length=40, db_index=True)),
                ('Name', models.CharField(max_length=96)),
                ('CreationTime', models.DateTimeField()),
                ('EntityJSON', jsonfield.fields.JSONField(default=dict)),
                ('ApplicationEnvironmentID', models.ForeignKey(to='glue2_db.ApplicationEnvironment', null=True)),
            ],
            options={
                'abstract': False,
                'db_name': 'glue2',
            },
        ),
        migrations.CreateModel(
            name='ComputingActivity',
            fields=[
                ('ID', models.CharField(max_length=120, serialize=False, primary_key=True)),
                ('ResourceID', models.CharField(max_length=40, db_index=True)),
                ('Name', models.CharField(max_length=96)),
                ('CreationTime', models.DateTimeField()),
                ('EntityJSON', jsonfield.fields.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
                'db_name': 'glue2',
            },
        ),
        migrations.CreateModel(
            name='ComputingManager',
            fields=[
                ('ID', models.CharField(max_length=120, serialize=False, primary_key=True)),
                ('ResourceID', models.CharField(max_length=40, db_index=True)),
                ('Name', models.CharField(max_length=96)),
                ('CreationTime', models.DateTimeField()),
                ('EntityJSON', jsonfield.fields.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
                'db_name': 'glue2',
            },
        ),
        migrations.CreateModel(
            name='ComputingShare',
            fields=[
                ('ID', models.CharField(max_length=120, serialize=False, primary_key=True)),
                ('ResourceID', models.CharField(max_length=40, db_index=True)),
                ('Name', models.CharField(max_length=96)),
                ('CreationTime', models.DateTimeField()),
                ('EntityJSON', jsonfield.fields.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
                'db_name': 'glue2',
            },
        ),
        migrations.CreateModel(
            name='Endpoint',
            fields=[
                ('ID', models.CharField(max_length=120, serialize=False, primary_key=True)),
                ('ResourceID', models.CharField(max_length=40, db_index=True)),
                ('Name', models.CharField(max_length=96)),
                ('CreationTime', models.DateTimeField()),
                ('EntityJSON', jsonfield.fields.JSONField(default=dict)),
                ('AbstractServiceID', models.ForeignKey(to='glue2_db.AbstractService')),
            ],
            options={
                'abstract': False,
                'db_name': 'glue2',
            },
        ),
        migrations.CreateModel(
            name='EntityHistory',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('DocumentType', models.CharField(max_length=32, db_index=True)),
                ('ResourceID', models.CharField(max_length=40, db_index=True)),
                ('ReceivedTime', models.DateTimeField()),
                ('EntityJSON', jsonfield.fields.JSONField(default=dict)),
            ],
            options={
                'db_name': 'glue2',
            },
        ),
        migrations.CreateModel(
            name='ExecutionEnvironment',
            fields=[
                ('ID', models.CharField(max_length=120, serialize=False, primary_key=True)),
                ('ResourceID', models.CharField(max_length=40, db_index=True)),
                ('Name', models.CharField(max_length=96)),
                ('CreationTime', models.DateTimeField()),
                ('EntityJSON', jsonfield.fields.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
                'db_name': 'glue2',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('ID', models.CharField(max_length=120, serialize=False, primary_key=True)),
                ('ResourceID', models.CharField(max_length=40, db_index=True)),
                ('Name', models.CharField(max_length=96)),
                ('CreationTime', models.DateTimeField()),
                ('EntityJSON', jsonfield.fields.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
                'db_name': 'glue2',
            },
        ),
    ]
