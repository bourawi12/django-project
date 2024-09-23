from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Listing
from .forms import ListingForm
from users.forms import LocationForm


def main_view(request):
    return render(request,'views/main.html', {"name":"autoMax"})

@login_required
def home_view(request):
    listings = Listing.objects.all()
    context = {
        'listings': listings,
    }
    return render(request, "views/home.html", context)  # Pass context here

@login_required
def list_view(request):
    if request.method == 'POST':
        pass
    elif request.method =='GET':
        listing_form = ListingForm()
        location_form = LocationForm()
    return render(request,'views/list.html', {'listing_form':listing_form,'location_form':location_form})
