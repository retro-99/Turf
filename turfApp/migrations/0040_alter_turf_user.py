# Generated by Django 4.2.6 on 2023-11-10 10:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('turfApp', '0039_remove_turf_advertisement_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turf',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
