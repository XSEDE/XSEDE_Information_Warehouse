# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-18 16:35
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('glue2_db', '0002_auto_20160629_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractservice',
            name='EntityJSON',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AlterField(
            model_name='applicationenvironment',
            name='EntityJSON',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AlterField(
            model_name='applicationhandle',
            name='EntityJSON',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AlterField(
            model_name='computingactivity',
            name='EntityJSON',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AlterField(
            model_name='computingmanager',
            name='EntityJSON',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AlterField(
            model_name='computingshare',
            name='EntityJSON',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AlterField(
            model_name='endpoint',
            name='EntityJSON',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AlterField(
            model_name='entityhistory',
            name='EntityJSON',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AlterField(
            model_name='executionenvironment',
            name='EntityJSON',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AlterField(
            model_name='location',
            name='EntityJSON',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
    ]
