# Generated by Django 5.1.6 on 2025-03-04 00:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="recipe",
            old_name="poster",
            new_name="poster_id",
        ),
    ]
