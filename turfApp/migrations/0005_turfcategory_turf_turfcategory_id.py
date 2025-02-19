# Generated by Django 4.2.6 on 2023-10-21 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('turfApp', '0004_profile_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='TurfCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('img', models.ImageField(blank=True, null=True, upload_to='uploads/images')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='turf',
            name='turfcategory_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='turfApp.turfcategory'),
        ),
    ]
