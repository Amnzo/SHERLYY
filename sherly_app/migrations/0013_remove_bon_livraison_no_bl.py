# Generated by Django 5.0.1 on 2024-01-21 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sherly_app', '0012_alter_bon_livraison_no_bl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bon_livraison',
            name='no_bl',
        ),
    ]
