# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glue2_db', '0005_applicationenvironment_appversion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationenvironment',
            name='AppVersion',
            field=models.CharField(default=b'none', max_length=32),
        ),
    ]
