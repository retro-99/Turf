# Generated by Django 4.2.6 on 2023-10-23 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('turfApp', '0011_alter_turf_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turf',
            name='user',
        ),
    ]
