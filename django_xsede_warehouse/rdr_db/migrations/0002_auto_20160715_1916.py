# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rdr_db', '0001_squashed_0003_auto_20160524_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rdrresource',
            name='parent_resource',
            field=models.ForeignKey(to='rdr_db.RDRResource', null=True, db_constraint=False),
        ),
    ]
