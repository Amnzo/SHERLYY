# Generated by Django 5.0.1 on 2024-02-24 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sherly_app", "0059_alter_bon_commande_add_d_alter_bon_commande_add_g"),
    ]

    operations = [
        migrations.AddField(
            model_name="table_bl",
            name="t2add",
            field=models.CharField(default="ADD", max_length=100),
        ),
    ]
