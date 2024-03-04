# Generated by Django 4.2.5 on 2024-03-03 08:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0031_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='seller_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
