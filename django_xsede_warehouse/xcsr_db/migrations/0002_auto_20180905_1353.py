# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-09-05 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xcsr_db', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentsprequirement',
            name='Requirement',
            field=models.CharField(choices=[('Required', 'Required'), ('Optional', 'Optional')], max_length=12),
        ),
        migrations.AlterField(
            model_name='componentsprequirement',
            name='SPClass',
            field=models.CharField(choices=[('XSEDE Level 1', 'XSEDE Level 1'), ('XSEDE Level 2', 'XSEDE Level 2'), ('XSEDE Level 3', 'XSEDE Level 3')], max_length=16),
        ),
    ]
