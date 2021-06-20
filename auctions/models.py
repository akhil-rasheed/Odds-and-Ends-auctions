from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class User(AbstractUser):
    pass

class Listing(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='listings_made')
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=400)
    starting_bid = models.DecimalField(max_digits=7, decimal_places=2)
    image_url = models.URLField()
    is_closed = models.BooleanField(default=False)
    watchlisted_users = models.ManyToManyField(User, related_name='watchlisted_posts', blank=True)
    CATEGORY_CHOICES = [
        ('TOYS', 'Toys'),
        ('ELECTRONICS', 'Electronics'),
        ('FURNITURE', 'Furniture'),
        ('CARS', 'Cars'),
        ('HOME', 'Home'),
        ('OTHERS', 'Others')
    ]
    category = models.CharField(max_length=13, choices=CATEGORY_CHOICES,
        default='OTHERS',)

    def current_price(self):
        return max([bid.bid_amount for bid in self.bids.all()] + [self.starting_bid])
    
    def bid_count(self):
        return len(self.bids.all())

    def highest_bidder(self):
        if self.bid_count() > 0:
            return self.bids.get(bid_amount=self.current_price()).bidder
        else:
            return None

    def __str__(self):
        return self.title
    

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='bids') 
    post = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids', blank=True)
    bid_amount = models.DecimalField(max_digits=7, decimal_places=2)

    def clean(self):
        print(self.bid_amount)
        print(self.post.current_price())
        if self.bid_amount and self.post.current_price():
            if self.bid_amount <= self.post.current_price():
                raise ValidationError({'bid_amount': ("Make a bid higher than the current price!")})

    
    def __str__(self):
        return f"User '{self.bidder}' offers {self.bid_amount} for {self.post}"

class Comment(models.Model):
    comment_text = models.CharField(max_length=300)
    post = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"User {self.commenter} says '{self.comment_text}'"



