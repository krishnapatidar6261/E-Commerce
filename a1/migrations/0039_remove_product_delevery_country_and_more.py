# Generated by Django 4.2.3 on 2024-05-23 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('a1', '0038_remove_order_order_id_order_deli'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='delevery_country',
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='deli',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='a1.delivery'),
        ),
    ]
