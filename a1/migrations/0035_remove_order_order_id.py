# Generated by Django 4.2.3 on 2024-05-23 05:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('a1', '0034_alter_order_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_id',
        ),
    ]
