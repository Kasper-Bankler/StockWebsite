# Generated by Django 5.0.3 on 2024-03-13 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_remove_portfolio_stock_remove_portfolio_buyingprice_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='price',
            field=models.FloatField(default=0, max_length=255),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='transaction_date',
            field=models.DateField(default=0, max_length=255),
        ),
    ]
