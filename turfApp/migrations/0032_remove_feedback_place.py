# Generated by Django 4.2.6 on 2023-11-07 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('turfApp', '0031_feedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='place',
        ),
    ]
