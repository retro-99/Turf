# Generated by Django 4.2.6 on 2023-11-02 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turfApp', '0028_alter_turf_multi_image_img_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
