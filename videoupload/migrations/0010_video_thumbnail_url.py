# Generated by Django 4.2.5 on 2023-10-26 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoupload', '0009_video_file_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='thumbnail_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]