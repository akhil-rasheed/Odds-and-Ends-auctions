from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("listing_new", views.listing_new_view, name="listing_new"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:listing_id>", views.listing_view, name="listing"),
    path("create_bid/<int:listing_id>", views.create_bid, name="create_bid"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("close_bids/<int:listing_id>", views.close_bids, name="close_bids"),
    path("category/<str:category>", views.category_view, name ='category_view'),
    path("search", views.search, name = "search"),
    path("add_watchlist/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist/<int:listing_id>", views.remove_watchlist, name='remove_watchlist'),
    path("watchlist", views.watchlist, name='watchlist'),
]
