# Generated by Django 4.2.6 on 2023-11-10 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('turfApp', '0038_turf_advertisement_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turf',
            name='advertisement_images',
        ),
    ]
