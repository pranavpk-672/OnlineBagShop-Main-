# Generated by Django 4.2.5 on 2024-03-31 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0038_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryassignment',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myauth.order'),
        ),
    ]
