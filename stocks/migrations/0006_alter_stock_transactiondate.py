# Generated by Django 5.0.3 on 2024-04-07 20:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stocks", "0005_alter_stock_ticker"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stock",
            name="transactionDate",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 4, 7, 20, 3, 23, 478541)
            ),
        ),
    ]
