# Generated by Django 4.1.2 on 2022-12-13 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonDRF', '0002_orders_deliveryprofile_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='delivery_status',
            field=models.BooleanField(default=False),
        ),
    ]
