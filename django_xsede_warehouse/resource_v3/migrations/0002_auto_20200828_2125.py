# Generated by Django 2.2.9 on 2020-08-28 21:25

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource_v3', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcev3',
            name='Audience',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='resourcev3',
            name='Description',
            field=models.CharField(blank=True, max_length=24000, null=True),
        ),
        migrations.AlterField(
            model_name='resourcev3',
            name='EndDateTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='resourcev3',
            name='Keywords',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='resourcev3',
            name='LocalID',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='resourcev3',
            name='ProviderID',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='resourcev3',
            name='ShortDescription',
            field=models.CharField(blank=True, max_length=1200, null=True),
        ),
        migrations.AlterField(
            model_name='resourcev3',
            name='StartDateTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='resourcev3',
            name='Topics',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='resourcev3local',
            name='CatalogMetaURL',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='resourcev3local',
            name='EntityJSON',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='resourcev3local',
            name='LocalID',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='resourcev3local',
            name='LocalType',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='resourcev3local',
            name='LocalURL',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]