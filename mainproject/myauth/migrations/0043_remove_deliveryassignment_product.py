# Generated by Django 4.2.5 on 2024-03-31 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0042_remove_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryassignment',
            name='product',
        ),
    ]