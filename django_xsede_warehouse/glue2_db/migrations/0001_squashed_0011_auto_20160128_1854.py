# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
#import jsonfield.fields
from django.contrib.postgres.fields import JSONField

class Migration(migrations.Migration):

    replaces = [
    ]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractService',
            fields=[
                ('ID', models.CharField(max_length=120, serialize=False, primary_key=True)),
                ('ResourceID', models.CharField(max_length=40, db_index=True)),
                ('Name', models.CharField(max_length=128, null=True)),
                ('CreationTime', models.DateTimeField()),
                ('EntityJSON', JSONField(default=dict)),
                ('ServiceType', models.CharField(max_length=32)),
                ('QualityLevel', models.CharField(max_length=16, null=True)),
                ('Type', models.CharField(default='', max_length=32)),
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
                ('Name', models.CharField(max_length=128, null=True)),
                ('CreationTime', models.DateTimeField()),
                ('EntityJSON', JSONField(default=dict)),
                ('AppName', models.CharField(default='', max_length=64)),
                ('Description', models.CharField(max_length=512, null=True)),
                ('AppVersion', models.CharField(default=b'none', max_length=64)),
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
                ('Name', models.CharField(max_length=128, null=True)),
                ('CreationTime', models.DateTimeField()),
                ('EntityJSON', JSONField(default=dict)),
                ('ApplicationEnvironment', models.ForeignKey(related_name='applicationhandles', to='glue2_db.ApplicationEnvironment', on_delete=models.CASCADE, null=True)),
                ('Type', models.CharField(default='', max_length=16)),
                ('Value', models.CharField(default='', max_length=64)),
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
                ('Name', models.CharField(max_length=128, null=True)),
                ('CreationTime', models.DateTimeField()),
                ('EntityJSON', JSONField(default=dict)),
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
                ('Name', models.CharField(max_length=128, null=True)),
                ('CreationTime', models.DateTimeField()),
                ('EntityJSON', JSONField(default=dict)),
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
                ('Name', models.CharField(max_length=128, null=True)),
                ('CreationTime', models.DateTimeField()),
                ('EntityJSON', JSONField(default=dict)),
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
                ('Name', models.CharField(max_length=128, null=True)),
                ('CreationTime', models.DateTimeField()),
                ('EntityJSON', JSONField(default=dict)),
                ('AbstractService', models.ForeignKey(related_name='endpoints', to='glue2_db.AbstractService', on_delete=models.CASCADE, null=True)),
                ('HealthState', models.CharField(default='', max_length=16)),
                ('InterfaceName', models.CharField(default='', max_length=32)),
                ('InterfaceVersion', models.CharField(default='', max_length=16)),
                ('QualityLevel', models.CharField(max_length=16, null=True)),
                ('ServingState', models.CharField(default='', max_length=16)),
                ('URL', models.CharField(default='', max_length=320)),
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
                ('EntityJSON', JSONField(default=dict)),
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
                ('Name', models.CharField(max_length=128, null=True)),
                ('CreationTime', models.DateTimeField()),
                ('EntityJSON', JSONField(default=dict)),
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
                ('Name', models.CharField(max_length=128, null=True)),
                ('CreationTime', models.DateTimeField()),
                ('EntityJSON', JSONField(default=dict)),
            ],
            options={
                'abstract': False,
                'db_name': 'glue2',
            },
        ),
    ]
