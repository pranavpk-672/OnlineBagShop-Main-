# Generated by Django 4.2.5 on 2024-03-08 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0033_coupon_visibility'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='datetime',
            field=models.TextField(default='empty'),
        ),
    ]
