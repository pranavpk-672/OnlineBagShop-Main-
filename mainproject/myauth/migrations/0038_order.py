# Generated by Django 4.2.5 on 2024-03-31 07:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0037_deliveryassignment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart', models.IntegerField(blank=True, null=True)),
                ('amount', models.IntegerField(default=0)),
                ('datetime', models.TextField(default='empty')),
                ('order_id_data', models.TextField(default='empty')),
                ('payment_id_data', models.TextField(default='empty')),
                ('status', models.CharField(default='pending', max_length=100)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
