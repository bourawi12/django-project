from django.db import models
import uuid
from .consts import CARS_BRANDS,TRANSMISSION_OPTIONS,DECISION
from users.models import Profile,Location
from .utils import user_listing_path
DECISION_CHOICES = [
    ('pending', 'pending'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ]

class Listing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE)
    brand = models.CharField(max_length=24)
    model = models.CharField(max_length=17)
    vin= models.CharField(max_length=17)
    mileage = models.IntegerField(default=0)
    color = models.CharField(max_length=17)
    description = models.TextField()
    engine = models.CharField(max_length=17)
    transmission = models.CharField(max_length=17)
    location = models.OneToOneField(Location,on_delete=models.SET_NULL,null=True)
    image = models.ImageField(upload_to=user_listing_path)
    decision = models.CharField(max_length=50, choices=DECISION_CHOICES, default='pending')
    cost = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.seller.user.username}\'s Listing - {self.model}'
    
class LikedListing(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.listing.model} listing likey by {self.profile.user.username} '