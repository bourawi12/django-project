from django import forms

from .models import Location

from localflavor.tn.forms import GOVERNORATE_CHOICES

class LocationForm(forms.ModelForm):
    
    class Meta :
        address_1 = forms.CharField(required=True)
        
        model = Location
        fields ={'address_1','address_2','city','state'}     