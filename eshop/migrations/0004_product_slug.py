# Generated by Django 5.1.2 on 2024-10-21 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("eshop", "0003_remove_category_description_category_slug_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="slug",
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
