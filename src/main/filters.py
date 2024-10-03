import django_filters
from .models import Listing

class ListingFilter(django_filters.FilterSet):
    class Meta:
        model = Listing
        fields = {
            'transmission': ['exact'],  # Filters for exact match
            'brand': ['exact'],         # Exact match for the brand
            'model': ['icontains'],     # Case-insensitive partial match for model
            'mileage': ['lt'],          # Less than comparison for mileage
        }
