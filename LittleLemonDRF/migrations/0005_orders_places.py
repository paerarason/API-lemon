# Generated by Django 4.1.2 on 2022-12-13 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonDRF', '0004_alter_deliveryprofile_orders_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='orders_places',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ManyToManyField(blank=True, related_name='OUT_FOR', to='LittleLemonDRF.orders')),
            ],
        ),
    ]
