# Generated by Django 4.2.6 on 2023-10-28 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('turfApp', '0027_alter_turf_multi_image_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turf_multi_image',
            name='img',
            field=models.FileField(blank=True, null=True, upload_to='uploads/images'),
        ),
        migrations.AlterField(
            model_name='turf_multi_image',
            name='turf',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='turfApp.turf'),
        ),
    ]
