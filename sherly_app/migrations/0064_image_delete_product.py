# Generated by Django 5.0.1 on 2024-03-27 13:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sherly_app", "0063_product"),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("desc", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="produit_images/"
                    ),
                ),
                (
                    "produit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sherly_app.produit",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Product",
        ),
    ]
