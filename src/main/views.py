from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
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
from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Listing
from .models import LikedListing, Listing,Profile
from .forms import ListingForm
from users.forms import LocationForm
from .filters import ListingFilter
def main_view(request):
    return render(request,'views/main.html', {"name":"autoMax"})

@login_required
def home_view(request):
    if request.user.is_staff:
        # Admin sees all listings
        listings = Listing.objects.all()
    else:
        # Regular users see only their own listings
        try:
            # Assuming you have a OneToOneField in Profile to User
            profile = Profile.objects.get(user=request.user)
            listings = Listing.objects.filter(seller=profile)  # Ensure this is the correct field name
        except Profile.DoesNotExist:
            listings = Listing.objects.none() 
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
        listing_form = ListingForm(request.POST, request.FILES, user=request.user)
        location_form = LocationForm(request.POST)

        if listing_form.is_valid() and location_form.is_valid():
            listing = listing_form.save(commit=False)
            listing.seller = request.user.profile
            listing.save()
            location_form.save()
            messages.info(request, f'{listing.model} Listing Posted successfully')
            return redirect('home')
    else:
        listing_form = ListingForm(user=request.user)  # Pass user here
        location_form = LocationForm()

    return render(request, 'views/list.html', {'listing_form': listing_form, 'location_form': location_form})

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
        
        if request.method == 'POST':
            listing_form = ListingForm(request.POST, request.FILES, instance=listing, user=request.user)
            location_form = LocationForm(request.POST, instance=listing.location)

            if listing_form.is_valid() and location_form.is_valid():
                listing_form.save()  # Save the listing form
                location_form.save()  # Save the location form
                
                messages.info(request, f'Listing {id} updated successfully!')
                return redirect('home')
            else:
                messages.error(request, 'An error occurred while trying to edit the listing.')
        else:
            listing_form = ListingForm(instance=listing, user=request.user)  # Pass user here
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

@login_required
@require_POST    
@staff_member_required
def accept_listing(request, id):
    if request.method == 'POST' and request.user.is_staff:
        listing = Listing.objects.get(id=id)
        listing.decision = 'accepted'
        listing.save()
        return redirect('home')  # Redirect after submission
    return redirect('home')

@login_required
@require_POST
@staff_member_required
def refuse_listing(request, id):
    if request.method == 'POST' and request.user.is_staff:
        listing = Listing.objects.get(id=id)
        listing.decision = 'refused'
        listing.save()
        return redirect('home')  # Redirect after submission
    return redirect('home')
@login_required
@staff_member_required
@require_POST
def delete_listing(request, id):
    # Fetch the listing by its ID, or return a 404 error if it doesn't exist
    listing = get_object_or_404(Listing, id=id)

    # Delete the listing
    listing.delete()

    # Add a success message
    messages.success(request, f'Listing {id} deleted successfully.')

    # Redirect back to the home page or listings page after deletion
    return redirect('home')
        

