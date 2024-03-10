# Generated by Django 4.2.5 on 2024-03-10 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0035_remove_coupon_datetime_coupon_expiration_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='CouponUsed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myauth.coupon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
