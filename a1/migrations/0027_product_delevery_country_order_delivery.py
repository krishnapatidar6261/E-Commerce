# Generated by Django 4.2.3 on 2024-05-11 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('a1', '0026_alter_product_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='delevery_country',
            field=models.TextField(choices=[('All Over World', 'All Over World'), ('India', 'India'), ('USA', 'USA'), ('UK', 'UK')], default='All Over World'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_qty', models.PositiveIntegerField(default=1)),
                ('product_price', models.PositiveIntegerField()),
                ('total_price', models.PositiveIntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a1.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a1.user')),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=20)),
                ('phone_number', models.PositiveIntegerField(max_length=20)),
                ('is_default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a1.user')),
            ],
        ),
    ]
