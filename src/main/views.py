from django.shortcuts import redirect, render ,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Listing
from .forms import ListingForm
from users.forms import LocationForm
from django.contrib import messages
from .filters import ListingFilter
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from imp import reload
from imp import reload
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail

from .models import LikedListing, Listing
from .forms import ListingForm
from users.forms import LocationForm
from .filters import ListingFilter
def main_view(request):
    return render(request,'views/main.html', {"name":"autoMax"})

@login_required
def home_view(request):
    listings = Listing.objects.all()
    listing_filter = ListingFilter(request.GET, queryset=listings)
    user_liked_listings = LikedListing.objects.filter(profile = request.user.profile).values_list('listing')
    liked_listings_ids = [l[0] for l in user_liked_listings]
    print(liked_listings_ids)
    context = {
        'listings': listings,
        'lisitng_filter':listing_filter,
        'liked_listings_ids':liked_listings_ids
    }
    return render(request, "views/home.html", context)  # Pass context here

@login_required
def list_view(request):
    if request.method == 'POST':
        try:
            listing_form = ListingForm(request.POST,request.FILES)
            location_form = LocationForm(request.POST,)
            if listing_form.is_valid() and location_form.is_valid():
                listing = listing_form.save(commit=False)
                listing_location= location_form.save()
                listing.seller = request.user.profile
                lislocation = listing_location
                listing.save()
                messages.info(request,f'{listing.model} Listing Posted successfully')
                return redirect('home')
        except Exception as e :
            print(e)
            messages.error(request,'error occured while posting')
    elif request.method =='GET':
        listing_form = ListingForm()
        location_form = LocationForm()
    return render(request,'views/list.html', {'listing_form':listing_form,'location_form':location_form})

@login_required
def listing_view(request, id):
    try :
        listing = Listing.objects.get(id=id)
        if listing is None : 
            raise Exception
        return render(request, 'views/lisitng.html', {'listing' : listing})
    except Exception as e :
        messages.error(request,f'invalid uid {id} was provided for listings')
        return redirect('home')
    
@login_required
def edit_view(request, id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        if request.method == 'POST':
            listing_form = ListingForm(request.POST, request.FILES, instance=listing)
            location_form = LocationForm(request.POST, instance=listing.location)
            
            # Make sure to call the is_valid() functions
            if listing_form.is_valid() and location_form.is_valid():
                print('Forms are valid')
                listing_form.save()  # Make sure this is not commented out
                location_form.save()
                
                messages.info(request, f'Listing {id} updated successfully!')
                return redirect('home')
            else:
                print(listing_form.errors)  # Print form errors to debug
                print(location_form.errors)
                messages.error(request, 'An error occurred while trying to edit the listing.')
        else:
            listing_form = ListingForm(instance=listing)
            location_form = LocationForm(instance=listing.location)
            
        context = {
            'location_form': location_form,
            'listing_form': listing_form,
        }
        return render(request, 'views/edit.html', context)

    except Exception as e:
        messages.error(request, f'An error occurred while trying to access the edit page: {e}')
        return redirect('home')


@login_required
def like_listing_view(request, id):
    listing = get_object_or_404(Listing, id=id)

    liked_listing, created = LikedListing.objects.get_or_create(
        profile=request.user.profile, listing=listing)

    if not created:
        liked_listing.delete()
    else:
        liked_listing.save()

    return JsonResponse({
        'is_liked_by_user': created,
    })
        
        

