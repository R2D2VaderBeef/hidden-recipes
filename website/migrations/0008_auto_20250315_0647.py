# Generated by Django 2.2.28 on 2025-03-14 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_merge_20250315_0053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_likes', to='website.Recipe'),
        ),
    ]
