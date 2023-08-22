from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("listings/<str:slug>", views.listing_page, name="listing_page"),
    path("comments/<str:slug>", views.comment, name="comment"),
    path("listings/<str:slug>/error", views.bid, name="bids"),
    path("categories", views.Categories.as_view(), name="categories"),
    path("categories/<str:slug>", views.category_listing, name="category_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist_add/<str:slug>", views.watchlist_add, name="watchlist_add"),
    path("watchlist_remove/<str:slug>", views.watchlist_remove, name="watchlist_remove"),
    path("close_listing/<str:slug>", views.close_listing, name="close_listing")
]
