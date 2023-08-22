from django import forms
from .models import Auction_Listing, Comment, Bid


class Auction_Listing_Form(forms.ModelForm):
    class Meta:
        model = Auction_Listing
        fields = ("title", "starting_bid", "auction_category", "description", "image_URL")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "starting_bid": forms.NumberInput(attrs={"class": "form-control", "placeholder": "00.00"}),
            "auction_category": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "id": "exampleFormControlTextarea1", "rows": "10"}),
            "image_URL": forms.TextInput(attrs={"class": "form-control", "placeholder": "(Optional)"}),
        }


class Comment_Form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", "rows": "5", "placeholder": "Write a comment..."}),
        }


class Bid_Form(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ("current_bid",)
        widgets = {
            "current_bid": forms.NumberInput(attrs={"class": "form-control", "placeholder": "00,00"}),
        }