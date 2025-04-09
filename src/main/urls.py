from django.conf import settings
from django.urls import path
from . import views
from .views import main_view, home_view , list_view, listing_view, edit_view,like_listing_view, accept_listing, refuse_listing

urlpatterns = [
    path('', main_view, name='main'),
    path('home/', home_view, name='home'),
    path('list/', list_view , name='list'),
    path('listing/<str:id>/', listing_view, name='listing'),
    path("listing/<str:id>/edit/", edit_view,name='edit'),
    path("listing/<str:id>/like/", like_listing_view,name='like_listing'),
    path('listing/<uuid:id>/accept/', views.accept_listing, name='accept_listing'),
    path('listing/<uuid:id>/refuse/', views.refuse_listing, name='refuse_listing'),
    path('delete-listing/<uuid:id>/', views.delete_listing, name='delete_listing')

    

]
