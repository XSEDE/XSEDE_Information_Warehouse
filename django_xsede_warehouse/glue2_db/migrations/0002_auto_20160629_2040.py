# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glue2_db', '0001_squashed_0011_auto_20160128_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractservice',
            name='Type',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='applicationenvironment',
            name='AppName',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='applicationhandle',
            name='Type',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='applicationhandle',
            name='Value',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='endpoint',
            name='HealthState',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='endpoint',
            name='InterfaceName',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='endpoint',
            name='InterfaceVersion',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='endpoint',
            name='ServingState',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='endpoint',
            name='URL',
            field=models.CharField(max_length=320),
        ),
    ]
