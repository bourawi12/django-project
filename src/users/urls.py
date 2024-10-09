from django.urls import path
from .views import login_view,RegisterView,logout_view,ProfileView
urlpatterns = [
   path('login/',login_view,name='login'),
   path('register/',RegisterView.as_view(),name='register'),
   path('logout/',logout_view,name='logout'),
   path('profile/', ProfileView.as_view(), name='profile'),
]
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
