# Generated by Django 5.0 on 2024-02-05 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turfApp', '0058_remove_booking_status_booking_booking_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='phonenumber',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
