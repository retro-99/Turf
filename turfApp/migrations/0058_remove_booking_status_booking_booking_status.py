# Generated by Django 4.2.6 on 2024-01-02 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turfApp', '0057_booking_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='status',
        ),
        migrations.AddField(
            model_name='booking',
            name='booking_status',
            field=models.IntegerField(choices=[(1, 'Active'), (0, 'Canceled')], default=1),
        ),
    ]
