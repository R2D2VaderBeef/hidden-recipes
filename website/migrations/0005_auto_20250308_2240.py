# Generated by Django 2.2.28 on 2025-03-08 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20250307_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(blank=True, default='defaults/default_profile.png', upload_to='profile_images'),
        ),
    ]
