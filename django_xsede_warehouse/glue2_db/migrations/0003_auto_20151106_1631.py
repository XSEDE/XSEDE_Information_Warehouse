# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glue2_db', '0002_auto_20151103_1709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='endpoint',
            name='AbstractServiceID',
        ),
        migrations.AddField(
            model_name='abstractservice',
            name='QualityLevel',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='abstractservice',
            name='Type',
            field=models.CharField(default='', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='endpoint',
            name='AbstractService',
            field=models.ForeignKey(related_name='endpoints', to='glue2_db.AbstractService', null=True),
        ),
        migrations.AddField(
            model_name='endpoint',
            name='HealthState',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='endpoint',
            name='InterfaceName',
            field=models.CharField(default='', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='endpoint',
            name='InterfaceVersion',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='endpoint',
            name='QualityLevel',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='endpoint',
            name='ServingState',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='endpoint',
            name='URL',
            field=models.CharField(default='', max_length=320),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='applicationhandle',
            name='ApplicationEnvironmentID',
            field=models.ForeignKey(related_name='handles', to='glue2_db.ApplicationEnvironment', null=True),
        ),
    ]
