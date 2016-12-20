# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glue2_db', '0008_auto_20151218_0411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationenvironment',
            name='AppVersion',
            field=models.CharField(default=b'none', max_length=64),
        ),
    ]
