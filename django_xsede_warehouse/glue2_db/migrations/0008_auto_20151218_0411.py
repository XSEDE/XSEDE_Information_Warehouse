# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glue2_db', '0007_auto_20151119_0413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractservice',
            name='Name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='applicationenvironment',
            name='Name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='applicationhandle',
            name='Name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='computingactivity',
            name='Name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='computingmanager',
            name='Name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='computingshare',
            name='Name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='endpoint',
            name='Name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='executionenvironment',
            name='Name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='Name',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
