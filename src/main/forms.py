from django import forms
import re
from .models import Listing

class ListingForm(forms.ModelForm):
    image = forms.ImageField(required=True)  # Define ImageField here, not in Meta

    class Meta:
        model = Listing
        fields = [#'brand',
                  #'model',
                  #'vin',
                  #'mileage',
                  #'color', 
                  'description',
                  #'engine',
                  #'transmission',
                  'image',
                  'decision',
                  'cost'
                  ]  # Use a list instead of a set
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Retrieve the user from kwargs
        super().__init__(*args, **kwargs)

        if user and not user.is_staff:
            # Disable 'decision' and 'cost' fields for non-admin users
            self.fields['decision'].disabled = True
            self.fields['cost'].disabled = False
