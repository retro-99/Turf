# Generated by Django 4.2.6 on 2023-10-28 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turfApp', '0026_alter_turf_multi_image_turf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turf_multi_image',
            name='img',
            field=models.FileField(upload_to='uploads/images'),
        ),
    ]
