# Generated by Django 2.2.28 on 2025-03-25 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_merge_20250321_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
