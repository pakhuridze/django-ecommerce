# Generated by Django 5.1.2 on 2024-10-20 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("eshop", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cartitem",
            old_name="card",
            new_name="cart",
        ),
    ]