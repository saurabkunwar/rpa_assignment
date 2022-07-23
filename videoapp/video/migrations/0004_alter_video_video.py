# Generated by Django 4.0.6 on 2022-07-23 05:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0003_alter_video_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(upload_to='video', validators=[django.core.validators.FileExtensionValidator(['mp4', 'mkv'])]),
        ),
    ]