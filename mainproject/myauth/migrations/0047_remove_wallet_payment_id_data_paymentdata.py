# Generated by Django 4.2.5 on 2024-04-06 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0046_wallet_payment_id_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='payment_id_data',
        ),
        migrations.CreateModel(
            name='PaymentData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myauth.wallet')),
            ],
        ),
    ]
