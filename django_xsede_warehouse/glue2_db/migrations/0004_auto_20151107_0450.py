# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glue2_db', '0003_auto_20151106_1631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicationhandle',
            name='ApplicationEnvironmentID',
        ),
        migrations.AddField(
            model_name='applicationenvironment',
            name='AppName',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='applicationenvironment',
            name='Description',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='applicationhandle',
            name='ApplicationEnvironment',
            field=models.ForeignKey(related_name='applicationhandles', to='glue2_db.ApplicationEnvironment', null=True),
        ),
        migrations.AddField(
            model_name='applicationhandle',
            name='Type',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='applicationhandle',
            name='Value',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]
