# Generated by Django 4.0.2 on 2022-03-09 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auction_listing_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listing',
            name='title',
            field=models.CharField(default=True, max_length=60),
        ),
    ]
