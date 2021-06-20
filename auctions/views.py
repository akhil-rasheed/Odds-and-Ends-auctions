from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from .models import User, Listing, Bid, Comment

from .forms import ListingForm, BidForm, CommentForm


def index(request):
    return render(request, "auctions/index.html", {
        "listings":Listing.objects.all()
    })


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

@login_required
def listing_new_view(request):
    if request.method == "POST":
        l_form = ListingForm(request.POST)
        if l_form.is_valid:
            listing_instance = l_form.save(commit=False)
            listing_instance.poster = request.user
            listing_instance.save()
            render(request, "auctions/index.html", {
                "message": "Listing added successfully"
            })
        else:
            l_form = ListingForm(request.POST)
            return render(request, "auctions/newlisting.html", {
                "form":l_form, "message":"Invalid data, please try again"
            })
    else:
        l_form = ListingForm()
        return render(request, "auctions/newlisting.html", {
            "form":l_form
        })
    return render(request, "auctions/newlisting.html")

def listing_view(request, listing_id, b_form=None):
    if not b_form:
            b_form = BidForm()
    listing = Listing.objects.get(id=listing_id)
    current_price = listing.current_price()
    highest_bidder = listing.highest_bidder()
    c_form = CommentForm()

    if request.user.is_authenticated:
        is_watchlisted = request.user.watchlisted_posts.filter(pk=listing_id).exists()
        is_poster = listing.poster == request.user
    else:
        is_watchlisted = None
        is_poster = None
    return render(request, "auctions/listing.html", {
        "listing":listing, "form":b_form, "current_price":current_price, "highest_bidder":highest_bidder, "c_form":c_form, "Comments":Comment.objects.filter(post=listing), "is_poster":is_poster, "is_watchlisted":is_watchlisted
    })

def category_view(request, category):
    listings_c = Listing.objects.filter(category= category)
    return render(request, "auctions/category.html", {
        "category":category, "listings":listings_c
    })

def search(request):
    if request.method=="POST":
        search_term = request.POST.get('term')
        listings_search = Listing.objects.filter(title__icontains=search_term)
        return render(request, "auctions/search.html", {
            "term":search_term, "listings":listings_search
        })

@login_required
def create_bid(request, listing_id):
    if request.method== "POST":
        listing = Listing.objects.get(pk=listing_id)
        bid = Bid(bidder=request.user, post=listing)
        b_form = BidForm(request.POST, instance=bid)
        if b_form.is_valid():
            b_form.save()
            messages.success(request, "Bid successfully made")
        else:
            return listing_view(request, listing_id, b_form=b_form)

        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def add_comment(request, listing_id):
    if request.method=="POST":
        listing = Listing.objects.get(pk=listing_id)
        comment =   Comment(commenter=request.user, post=listing)
        c_form = CommentForm(request.POST, instance=comment)
        if c_form.is_valid:
            c_form.save()
            messages.success(request, "Comment made!")
        else:
            return render(request, reverse("listing"), listing_id, c_form = c_form)

        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def close_bids(request, listing_id):
    assert request.user.is_authenticated
    if request.method=="POST":
        listing = Listing.objects.get(pk=listing_id)
        if listing.poster == request.user:           
            listing.is_closed = True
            listing.save()
            messages.success(request, "Bids for this listing are now closed!")
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))    

@login_required
def add_watchlist(request, listing_id):
    assert request.user.is_authenticated
    if request.method=="POST":
        listing = Listing.objects.get(pk=listing_id)
        listing.watchlisted_users.add(request.user)
        listing.save()
        messages.success(request, "Item added to watchlist")
    return HttpResponseRedirect(reverse("listing", args=(listing_id,))) 

@login_required
def remove_watchlist(request, listing_id):
    assert request.user.is_authenticated
    if request.method=="POST":
        listing = Listing.objects.get(pk=listing_id)
        if request.user.watchlisted_posts.filter(pk=listing_id).exists():
            listing.watchlisted_users.remove(request.user)
            listing.save()
            messages.info(request, "Item removed from watchlist")
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required
def watchlist(request):
    listings_w = request.user.watchlisted_posts.all()
    return render(request, "auctions/watchlist.html", {
    "listings":listings_w, "user":request.user
    })