# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-24 16:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glue2_db', '0008_computingqueue'),
    ]

    operations = [
        migrations.AddField(
            model_name='admindomain',
            name='Distributed',
            field=models.NullBooleanField(),
        ),
    ]
