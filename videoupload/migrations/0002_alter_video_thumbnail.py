# Generated by Django 4.2.5 on 2023-10-10 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoupload', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='videos/'),
        ),
    ]