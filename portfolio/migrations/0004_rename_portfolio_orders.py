# Generated by Django 5.0.3 on 2024-03-13 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_options_alter_customuser_groups_and_more'),
        ('portfolio', '0003_alter_portfolio_price_and_more'),
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Portfolio',
            new_name='Orders',
        ),
    ]