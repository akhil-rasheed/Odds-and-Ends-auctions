from .models import Listing, Bid, Comment
from django.forms import ModelForm

#Form for Listing
class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']