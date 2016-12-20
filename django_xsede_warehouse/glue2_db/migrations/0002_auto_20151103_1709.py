# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glue2_db', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationhandle',
            name='ApplicationEnvironmentID',
            field=models.ForeignKey(related_name='applicationhandleid', to='glue2_db.ApplicationEnvironment', null=True),
        ),
        migrations.AlterField(
            model_name='endpoint',
            name='AbstractServiceID',
            field=models.ForeignKey(related_name='abstractserviceid', to='glue2_db.AbstractService', null=True),
        ),
    ]
