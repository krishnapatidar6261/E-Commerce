# Generated by Django 4.2.3 on 2024-05-23 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a1', '0029_rename_address_delivery_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_approve',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.TextField(default=None),
        ),
        migrations.AddField(
            model_name='order',
            name='transaction_id',
            field=models.TextField(default=None),
        ),
    ]
