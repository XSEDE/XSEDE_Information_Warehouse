# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rdr_db', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rdrresource',
            name='access_description',
            field=models.CharField(max_length=4000, null=True),
        ),
    ]
