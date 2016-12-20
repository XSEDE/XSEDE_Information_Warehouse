# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='speedpage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('tstamp', models.IntegerField(null=True)),
                ('sourceid', models.CharField(max_length=32)),
                ('source', models.CharField(max_length=120, db_index=True)),
                ('src_url', models.CharField(max_length=320)),
                ('destid', models.CharField(max_length=40, db_index=True)),
                ('dest', models.CharField(max_length=40, db_index=True)),
                ('dest_url', models.CharField(max_length=320)),
                ('xfer_rate', models.CharField(max_length=32)),
            ],
            options={
                'db_name': 'xcsr',
            },
        ),
    ]
