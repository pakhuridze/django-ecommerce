# Generated by Django 5.1.2 on 2024-11-07 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("eshop", "0006_category_name_en_category_name_ka"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="category",
            name="name_en",
        ),
        migrations.RemoveField(
            model_name="category",
            name="name_ka",
        ),
    ]
