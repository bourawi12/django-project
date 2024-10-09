from django import forms
from dataclasses import field
from .models import Location
from django.contrib.auth.models import User
from localflavor.tn.forms import GOVERNORATE_CHOICES
from .models import Location, Profile
from .widgets import CustomPictureImageFieldWidget

class UserForm(forms.ModelForm):
    username = forms.CharField(disabled=True)
    
    class Meta : 
        model = User
        fields = ('username', 'first_name', 'last_name')

class ProfileForm(forms.ModelForm):
    photo = forms.ImageField(widget=CustomPictureImageFieldWidget)
    bio = forms.TextInput()
    
    class Meta : 
        model = Profile
        fields = ('photo', 'bio','phone_number')
class LocationForm(forms.ModelForm):
    
    class Meta :
        address_1 = forms.CharField(required=True)
        
        model = Location
        fields ={'address_1','address_2','city','state'}     