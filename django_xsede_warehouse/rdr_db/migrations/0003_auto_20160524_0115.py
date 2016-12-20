# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rdr_db', '0002_auto_20160524_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rdrresource',
            name='recommended_use',
            field=models.CharField(max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='rdrresource',
            name='resource_description',
            field=models.CharField(max_length=4000, null=True),
        ),
    ]
