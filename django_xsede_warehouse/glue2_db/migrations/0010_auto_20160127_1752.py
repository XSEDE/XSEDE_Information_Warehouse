# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glue2_db', '0009_auto_20160126_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractservice',
            name='QualityLevel',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='endpoint',
            name='QualityLevel',
            field=models.CharField(max_length=16, null=True),
        ),
    ]
