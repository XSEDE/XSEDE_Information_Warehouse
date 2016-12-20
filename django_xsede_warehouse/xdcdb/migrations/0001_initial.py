# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TGResource',
            fields=[
                ('ResourceID', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('SiteID', models.CharField(max_length=40, db_index=True)),
                ('OrganizationAbbrev', models.CharField(max_length=40, db_index=True)),
                ('OrganizationName', models.CharField(max_length=120, db_index=True)),
                ('AmieName', models.CharField(max_length=40, db_index=True)),
                ('PopsName', models.CharField(max_length=120, db_index=True)),
                ('TgcdbResourceName', models.CharField(max_length=40, db_index=True)),
                ('ResourceCode', models.CharField(max_length=40, db_index=True)),
                ('ResourceDescription', models.CharField(max_length=40, db_index=True)),
                ('Timestamp', models.DateTimeField(null=True)),
            ],
            options={
                'db_name': 'xcsr',
            },
        ),
    ]
