# Generated by Django 3.0.4 on 2020-04-09 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_auto_20200409_1618'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockprice',
            name='per',
        ),
    ]
