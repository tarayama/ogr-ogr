# Generated by Django 3.1 on 2020-10-03 13:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ogr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ogr_ogr',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 10, 3, 22, 48, 37, 525598)),
        ),
    ]