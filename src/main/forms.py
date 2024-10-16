from django import forms
import re
from .models import Listing

class ListingForm(forms.ModelForm):
    
    class Meta :
        image = forms.ImageField(required=True)
        
        model = Listing
        fields ={'brand','model','vin','mileage','color',
                 'description','engine','transmission','image'}     