# Generated by Django 4.2.5 on 2023-12-12 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ott', '0002_rename_uploadedcontent_ott'),
    ]

    operations = [
        migrations.AddField(
            model_name='ott',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
