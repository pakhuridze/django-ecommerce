# Generated by Django 5.1.2 on 2024-10-24 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("eshop", "0006_product_image_poi_alter_product_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="image_poi",
        ),
    ]
