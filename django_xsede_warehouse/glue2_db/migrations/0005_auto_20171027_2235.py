# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-27 22:35
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glue2_db', '0004_auto_20170106_2148'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessPolicy',
            fields=[
                ('ID', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=128, null=True)),
                ('CreationTime', models.DateTimeField()),
                ('Validity', models.DurationField(null=True)),
                ('EntityJSON', django.contrib.postgres.fields.jsonb.JSONField()),
                ('Scheme', models.CharField(max_length=16, null=True)),
                ('Rule', models.CharField(max_length=128, null=True)),
            ],
            options={
                'abstract': False,
                'db_name': 'glue2',
            },
        ),
        migrations.CreateModel(
            name='AdminDomain',
            fields=[
                ('ID', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=128, null=True)),
                ('CreationTime', models.DateTimeField()),
                ('Validity', models.DurationField(null=True)),
                ('EntityJSON', django.contrib.postgres.fields.jsonb.JSONField()),
                ('Description', models.CharField(max_length=128, null=True)),
                ('WWW', models.URLField(null=True)),
                ('Owner', models.CharField(max_length=128, null=True)),
            ],
            options={
                'abstract': False,
                'db_name': 'glue2',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('ID', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=128, null=True)),
                ('CreationTime', models.DateTimeField()),
                ('Validity', models.DurationField(null=True)),
                ('EntityJSON', django.contrib.postgres.fields.jsonb.JSONField()),
                ('Detail', models.CharField(max_length=128)),
                ('Type', models.CharField(max_length=16)),
            ],
            options={
                'abstract': False,
                'db_name': 'glue2',
            },
        ),
        migrations.CreateModel(
            name='UserDomain',
            fields=[
                ('ID', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=128, null=True)),
                ('CreationTime', models.DateTimeField()),
                ('Validity', models.DurationField(null=True)),
                ('EntityJSON', django.contrib.postgres.fields.jsonb.JSONField()),
                ('Description', models.CharField(max_length=128, null=True)),
                ('WWW', models.URLField(null=True)),
                ('Level', models.PositiveIntegerField(null=True)),
                ('UserManager', models.URLField(null=True)),
                ('Member', models.CharField(max_length=128, null=True)),
            ],
            options={
                'abstract': False,
                'db_name': 'glue2',
            },
        ),
        migrations.RemoveField(
            model_name='location',
            name='ResourceID',
        ),
        migrations.AddField(
            model_name='abstractservice',
            name='Validity',
            field=models.DurationField(null=True),
        ),
        migrations.AddField(
            model_name='applicationenvironment',
            name='Validity',
            field=models.DurationField(null=True),
        ),
        migrations.AddField(
            model_name='applicationhandle',
            name='Validity',
            field=models.DurationField(null=True),
        ),
        migrations.AddField(
            model_name='computingactivity',
            name='Validity',
            field=models.DurationField(null=True),
        ),
        migrations.AddField(
            model_name='computingmanager',
            name='Validity',
            field=models.DurationField(null=True),
        ),
        migrations.AddField(
            model_name='computingshare',
            name='Validity',
            field=models.DurationField(null=True),
        ),
        migrations.AddField(
            model_name='endpoint',
            name='Validity',
            field=models.DurationField(null=True),
        ),
        migrations.AddField(
            model_name='executionenvironment',
            name='Validity',
            field=models.DurationField(null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='Address',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='Country',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='Latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='Longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='Place',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='PostCode',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='Validity',
            field=models.DurationField(null=True),
        ),
    ]