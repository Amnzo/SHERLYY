# Generated by Django 5.0.1 on 2024-01-21 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sherly_app', '0008_remove_bon_livraison_no_bl'),
    ]

    operations = [
        migrations.AddField(
            model_name='bon_livraison',
            name='no_bl',
            field=models.CharField(default='DEFAULT_VALUE', editable=False, max_length=20, unique=True),
        ),
    ]
