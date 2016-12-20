# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    replaces = [(b'glue2_db', '0001_initial'), (b'glue2_db', '0002_auto_20151103_1709'), (b'glue2_db', '0003_auto_20151106_1631'), (b'glue2_db', '0004_auto_20151107_0450'), (b'glue2_db', '0005_applicationenvironment_appversion'), (b'glue2_db', '0006_auto_20151119_0017'), (b'glue2_db', '0007_auto_20151119_0413'), (b'glue2_db', '0008_auto_20151218_0411'), (b'glue2_db', '0009_auto_20160126_2331'), (b'glue2_db', '0010_auto_20160127_1752'), (b'glue2_db', '0011_auto_20160128_1854')]

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
                ('EntityJSON', jsonfield.fields.JSONField(default=dict)),
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
                ('EntityJSON', jsonfield.fields.JSONField(default=dict)),
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
                ('EntityJSON', jsonfield.fields.JSONField(default=dict)),
                ('ApplicationEnvironment', models.ForeignKey(related_name='applicationhandles', to='glue2_db.ApplicationEnvironment', null=True)),
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
                ('Name', models.CharField(max_length=128, null=True)),
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
                ('Name', models.CharField(max_length=128, null=True)),
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
                ('Name', models.CharField(max_length=128, null=True)),
                ('CreationTime', models.DateTimeField()),
                ('EntityJSON', jsonfield.fields.JSONField(default=dict)),
                ('AbstractService', models.ForeignKey(related_name='endpoints', to='glue2_db.AbstractService', null=True)),
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
                ('Name', models.CharField(max_length=128, null=True)),
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
                ('Name', models.CharField(max_length=128, null=True)),
                ('CreationTime', models.DateTimeField()),
                ('EntityJSON', jsonfield.fields.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
                'db_name': 'glue2',
            },
        ),
    ]
