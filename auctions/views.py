from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView, CreateView
from numpy import save
from .models import Auction_Listing, Bid
from .forms import *
from django.contrib.auth.decorators import login_required

from .models import Category, User


class Index(ListView):
    model = Auction_Listing
    ordering = ["-created"]
    template_name = "auctions/index.html"


class Categories(ListView):
    model = Category
    template_name = "auctions/categories.html"


@login_required
def new_listing(request):
    if request.method == "POST":
        form = Auction_Listing_Form(request.POST)
        if form.is_valid():
            new_auction_listing = form.save()
            if new_auction_listing.image_URL == None:
                new_auction_listing.image_URL = "https://t4.ftcdn.net/jpg/02/51/95/53/360_F_251955356_FAQH0U1y1TZw3ZcdPGybwUkH90a3VAhb.jpg"
            new_auction_listing.author = request.user
            new_auction_listing.save()
            return render(request, "auctions/new_listing.html", {
                "message": True,
                "auction_form": Auction_Listing_Form
            })
    else:
        return render(request, "auctions/new_listing.html", {
            "auction_form": Auction_Listing_Form
        })



def category_listing(request, slug):
    category = Category.objects.get(slug=slug)
    return render(request, "auctions/category_listing.html", {
        "category": category
    })


def listing_page(request, slug):
    listing = Auction_Listing.objects.get(slug=slug)
    if request.user in listing.watchlist.all():
        it_is = True
    else:
        it_is = False
    return render(request, "auctions/listing_page.html", {
        "it_is": it_is,
        "listing": listing,
        "bid": Bid_Form,
        "comment_form": Comment_Form
    })


def close_listing(request, slug):
    listing = Auction_Listing.objects.get(slug=slug)
    if request.user == listing.author:
        listing.is_active = False
        listing.winner = listing.current_user_bid
        listing.watchlist.clear()
        listing.save()
        return HttpResponseRedirect(reverse("listing_page", args=[slug]))
    else:
        return HttpResponseRedirect(reverse("listing_page", args=[slug]))


@login_required
def comment(request, slug):
    listing = Auction_Listing.objects.get(slug=slug)
    form = Comment_Form(request.POST)
    Comment = form.save(commit=False)
    Comment.user = request.user
    Comment.auction = listing
    Comment.save()
    return HttpResponseRedirect(reverse("listing_page", args=[slug]))


@login_required
def bid(request, slug):
    listing = Auction_Listing.objects.get(slug=slug)
    if listing.is_active:
        if not request.user == listing.author:
            bid_request = float(request.POST["current_bid"])
            if bid_request >= listing.starting_bid and (listing.current_bid_validate == None or bid_request > listing.current_bid_validate):
                listing.current_bid_validate = bid_request
                form = Bid_Form(request.POST)
                Bid = form.save(commit=False)
                listing.current_user_bid = request.user
                Bid.user = request.user
                Bid.auction = listing
                Bid.save()
                listing.save()
                return HttpResponseRedirect(reverse("listing_page", args=[slug]))
            else:
                return render(request, "auctions/listing_page.html", {
                "listing": listing,
                "bid": Bid_Form,
                "comment_form": Comment_Form,
                "invalid_value": True
            })
        else:
            return render(request, "auctions/listing_page.html", {
                "listing": listing,
                "bid": Bid_Form,
                "comment_form": Comment_Form,
                "invalid_user": True 
            })
    else:
        return render(request, "auctions/listing_page.html", {
            "listing": listing,
            "bid": Bid_Form,
            "comment_form": Comment_Form,
            "sold": True
        })


@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html")


@login_required
def watchlist_add(request, slug):
    listing = Auction_Listing.objects.get(slug=slug)
    if listing.is_active:
        if not request.user == listing.author:
            listing.watchlist.add(request.user)
            return HttpResponseRedirect(reverse("listing_page", args=[slug]))
        else:
            return HttpResponseRedirect(reverse("listing_page", args=[slug]))
    else:
        return HttpResponseRedirect(reverse("listing_page", args=[slug]))


@login_required
def watchlist_remove(request, slug):
    listing = Auction_Listing.objects.get(slug=slug)
    if listing.is_active:
        if not request.user == listing.author:
            listing.watchlist.remove(request.user)
            return HttpResponseRedirect(reverse("listing_page", args=[slug]))
        else:
            return HttpResponseRedirect(reverse("listing_page", args=[slug])) 
    else:
        return HttpResponseRedirect(reverse("listing_page", args=[slug]))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
