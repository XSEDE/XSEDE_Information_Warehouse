# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glue2_db', '0010_auto_20160127_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractservice',
            name='ServiceType',
            field=models.CharField(max_length=32),
        ),
    ]
