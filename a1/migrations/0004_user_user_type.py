# Generated by Django 4.2.3 on 2023-07-28 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a1', '0003_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(default='buyer', max_length=50),
        ),
    ]
