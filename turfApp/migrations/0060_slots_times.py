# Generated by Django 5.0 on 2024-02-05 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turfApp', '0059_booking_phonenumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='slots',
            name='times',
            field=models.TimeField(default='6:00'),
            preserve_default=False,
        ),
    ]
