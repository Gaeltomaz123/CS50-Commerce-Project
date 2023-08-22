from django.contrib import admin
from .models import *


class Auction_Listing_Admin(admin.ModelAdmin):
    list_display = ("title","auction_category","author", "created")


# Register your models here.
admin.site.register(Category)
admin.site.register(Auction_Listing)
admin.site.register(Bid)
admin.site.register(Comment)