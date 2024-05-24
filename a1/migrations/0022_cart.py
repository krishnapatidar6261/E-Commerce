# Generated by Django 4.2.3 on 2023-08-10 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('a1', '0021_alter_user_profile_pic_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_qty', models.PositiveIntegerField(default=1)),
                ('product_price', models.PositiveIntegerField()),
                ('payment_status', models.BooleanField(default=False)),
                ('total_price', models.PositiveIntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a1.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a1.user')),
            ],
        ),
    ]