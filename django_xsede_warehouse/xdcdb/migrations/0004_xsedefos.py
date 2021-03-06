# Generated by Django 2.2.9 on 2020-09-30 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xdcdb', '0003_xsedeperson'),
    ]

    operations = [
        migrations.CreateModel(
            name='XSEDEFos',
            fields=[
                ('field_of_science_id', models.IntegerField(primary_key=True, serialize=False)),
                ('parent_field_of_science_id', models.IntegerField(blank=True, null=True)),
                ('field_of_science_desc', models.CharField(max_length=200)),
                ('fos_nsf_id', models.IntegerField(blank=True, null=True)),
                ('fos_nsf_abbrev', models.CharField(blank=True, max_length=10, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_name': 'xcsr',
            },
        ),
    ]
