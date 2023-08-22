# Generated by Django 4.0.2 on 2022-03-13 05:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auction_listing_created_auction_listing_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listing',
            name='auction_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_auction', to='auctions.category'),
        ),
        migrations.AlterField(
            model_name='auction_listing',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='auction_listing',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='auction_listing',
            name='description',
            field=models.TextField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='auction_listing',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
