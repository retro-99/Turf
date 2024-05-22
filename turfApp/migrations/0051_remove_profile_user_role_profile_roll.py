# Generated by Django 4.1.4 on 2023-12-07 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turfApp', '0050_remove_post_admin_whtsappnumber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user_role',
        ),
        migrations.AddField(
            model_name='profile',
            name='roll',
            field=models.CharField(choices=[('user', 'user'), ('owner', 'owner')], default='user', max_length=7),
        ),
    ]
