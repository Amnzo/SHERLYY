# Generated by Django 5.0.1 on 2024-02-08 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sherly_app", "0044_invoice"),
    ]

    operations = [
        migrations.AddField(
            model_name="facture",
            name="remarque",
            field=models.TextField(default=""),
        ),
    ]
