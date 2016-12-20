# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glue2_db', '0004_auto_20151107_0450'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationenvironment',
            name='AppVersion',
            field=models.CharField(default=0, max_length=32),
            preserve_default=False,
        ),
    ]
