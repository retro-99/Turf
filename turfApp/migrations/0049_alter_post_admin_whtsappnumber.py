# Generated by Django 4.2.6 on 2023-11-14 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turfApp', '0048_alter_post_admin_whtsappnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='admin_whtsappnumber',
            field=models.IntegerField(default=0),
        ),
    ]
