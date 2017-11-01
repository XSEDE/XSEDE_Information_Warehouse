# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-01 10:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glue2_db', '0006_add_accelerator_models'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='acceleratorenvironment',
            name='ComputeCapacity',
        ),
        migrations.RemoveField(
            model_name='acceleratorenvironment',
            name='LogicalAccelerators',
        ),
        migrations.RemoveField(
            model_name='acceleratorenvironment',
            name='Model',
        ),
        migrations.RemoveField(
            model_name='acceleratorenvironment',
            name='PhysicalAccelerators',
        ),
        migrations.RemoveField(
            model_name='acceleratorenvironment',
            name='Vendor',
        ),
        migrations.RemoveField(
            model_name='acceleratorenvironment',
            name='Version',
        ),
        migrations.RemoveField(
            model_name='accesspolicy',
            name='Rule',
        ),
        migrations.RemoveField(
            model_name='accesspolicy',
            name='Scheme',
        ),
        migrations.RemoveField(
            model_name='computingmanageracceleratorinfo',
            name='TotalAcceleratorsSlots',
        ),
        migrations.RemoveField(
            model_name='computingmanageracceleratorinfo',
            name='TotalPhysicalAccelerators',
        ),
        migrations.RemoveField(
            model_name='computingmanageracceleratorinfo',
            name='UsedAcceleratorSlots',
        ),
        migrations.RemoveField(
            model_name='computingshareacceleratorinfo',
            name='FreeAcceleratorSlots',
        ),
        migrations.RemoveField(
            model_name='computingshareacceleratorinfo',
            name='MaxAcceleratorSlotsPerJob',
        ),
        migrations.RemoveField(
            model_name='computingshareacceleratorinfo',
            name='UsedAcceleratorSlots',
        ),
        migrations.RemoveField(
            model_name='location',
            name='Address',
        ),
        migrations.RemoveField(
            model_name='location',
            name='Country',
        ),
        migrations.RemoveField(
            model_name='location',
            name='Latitude',
        ),
        migrations.RemoveField(
            model_name='location',
            name='Longitude',
        ),
        migrations.RemoveField(
            model_name='location',
            name='Place',
        ),
        migrations.RemoveField(
            model_name='location',
            name='PostCode',
        ),
        migrations.RemoveField(
            model_name='userdomain',
            name='Level',
        ),
        migrations.RemoveField(
            model_name='userdomain',
            name='Member',
        ),
        migrations.RemoveField(
            model_name='userdomain',
            name='UserManager',
        ),
        migrations.AlterField(
            model_name='entityhistory',
            name='ResourceID',
            field=models.CharField(db_index=True, max_length=40, null=True),
        ),
    ]
