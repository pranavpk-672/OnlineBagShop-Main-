# Generated by Django 4.2.5 on 2023-11-25 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0014_product_brand_name_product_product_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product_review',
            name='product_id',
        ),
        migrations.RemoveField(
            model_name='product_review',
            name='user',
        ),
        migrations.DeleteModel(
            name='product_rating',
        ),
        migrations.DeleteModel(
            name='product_review',
        ),
    ]
