from django import forms
import re
from .models import Listing

class ListingForm(forms.ModelForm):
    image = forms.ImageField(required=True)  # Define ImageField here, not in Meta

    class Meta:
        model = Listing
        fields = ['brand', 'model', 'vin', 'mileage', 'color', 
                  'description', 'engine', 'transmission', 'image']  # Use a list instead of a set
