# Generated by Django 2.2.28 on 2025-03-14 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_auto_20250315_0647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
