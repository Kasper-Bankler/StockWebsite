# Generated by Django 5.0.3 on 2024-04-11 10:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stocks", "0007_alter_stock_transactiondate"),
    ]

    operations = [
        migrations.DeleteModel(name="Sector",),
        migrations.AlterField(
            model_name="stock",
            name="transactionDate",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 4, 11, 10, 41, 44, 367009)
            ),
        ),
    ]
