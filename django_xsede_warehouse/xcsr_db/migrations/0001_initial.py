# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ComponentSPRequirement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ComponentName', models.CharField(max_length=64)),
                ('SPClass', models.CharField(max_length=16, choices=[(b'XSEDE Level 1', b'XSEDE Level 1'), (b'XSEDE Level 2', b'XSEDE Level 2'), (b'XSEDE Level 3', b'XSEDE Level 3')])),
                ('Requirement', models.CharField(max_length=12, choices=[(b'Required', b'Required'), (b'Optional', b'Optional')])),
                ('UpdateTime', models.DateTimeField(auto_now=True)),
                ('UpdateUser', models.CharField(max_length=16)),
            ],
            options={
                'db_name': 'xcsr',
            },
        ),
        migrations.AlterUniqueTogether(
            name='componentsprequirement',
            unique_together=set([('ComponentName', 'SPClass')]),
        ),
    ]
