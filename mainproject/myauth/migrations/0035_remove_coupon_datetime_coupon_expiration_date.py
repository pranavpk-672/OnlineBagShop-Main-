# Generated by Django 4.2.5 on 2024-03-10 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0034_coupon_datetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='datetime',
        ),
        migrations.AddField(
            model_name='coupon',
            name='expiration_date',
            field=models.DateField(default='2099-12-31'),
        ),
    ]
