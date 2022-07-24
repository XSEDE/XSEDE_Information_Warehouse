# Generated by Django 2.2.24 on 2022-07-24 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outages', '0003_auto_20220723_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outages',
            name='Content',
            field=models.CharField(max_length=8000),
        ),
        migrations.AlterField(
            model_name='outages',
            name='OutageID',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='outages',
            name='ResourceID',
            field=models.CharField(db_index=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='outages',
            name='Subject',
            field=models.CharField(max_length=120),
        ),
    ]
