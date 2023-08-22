from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=30)
    slug = models.SlugField('Slug', editable=False)


    def __str__(self):
        return f"{self.category}"


    def save(self, *args, **kwargs):
        url = self.category
        self.slug = slugify(url, allow_unicode=True)
        super().save(*args, **kwargs)


class Auction_Listing(models.Model):
    title = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    starting_bid = models.FloatField()
    current_bid_validate = models.FloatField(blank=True, null=True)
    auction_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_auction", blank=True, null=True)
    description = models.TextField(max_length=150)
    image_URL = models.CharField(max_length=500, blank=True, null=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist_users")
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="listing_author")
    current_user_bid = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name="listing_normal_users")
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name="winner")
    slug = models.SlugField('Slug', editable=False)


    def __str__(self):
        return f"{self.title} | {self.auction_category} | {self.author} | {self.current_bid_validate}"


    def save(self, *args, **kwargs):
        url = self.title
        self.slug = slugify(url, allow_unicode=True)
        super().save(*args, **kwargs)

    
    def get_absolute_url(self):
        return f"/listings/{ self.slug }"


class Bid(models.Model):
    auction = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_bid = models.FloatField()

class Comment(models.Model):
    auction = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=550)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.auction.title} | {self.user}"