# Generated by Django 4.1.7 on 2023-05-03 17:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Store", "0005_alter_product_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.CharField(
                choices=[
                    ("S", "Shirt"),
                    ("P", "Pants"),
                    ("J", "Sweater"),
                    ("SW", "Sweatshirt"),
                    ("SH", "Shoes"),
                    ("A", "Accessories"),
                    ("O", "Other"),
                ],
                max_length=2,
                verbose_name="Категория",
            ),
        ),
    ]
