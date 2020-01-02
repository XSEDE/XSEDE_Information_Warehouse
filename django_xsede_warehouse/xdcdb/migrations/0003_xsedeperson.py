# Generated by Django 2.2.7 on 2019-12-21 00:41

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xdcdb', '0002_auto_20190509_1810'),
    ]

    operations = [
        migrations.CreateModel(
            name='XSEDEPerson',
            fields=[
                ('person_id', models.IntegerField(primary_key=True, serialize=False)),
                ('portal_login', models.CharField(db_index=True, max_length=30)),
                ('last_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(max_length=60, null=True)),
                ('is_suspended', models.BooleanField()),
                ('organization', models.CharField(max_length=300)),
                ('citizenships', models.CharField(max_length=300, null=True)),
                ('emails', models.CharField(max_length=300, null=True)),
                ('addressesJSON', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
            options={
                'db_name': 'xcsr',
            },
        ),
    ]
