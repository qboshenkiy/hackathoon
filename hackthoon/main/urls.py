from django.urls import path
from .views import login_view, view_profile, edit_profile, home, logout_view, search_users
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),  
    path('login/', login_view, name='login'), 
    path('profile/', view_profile, name='profile_view'),  
    path('profile/edit/', edit_profile, name='profile_edit'),  
    path('logout/', logout_view, name='logout'),
    path('search/', search_users, name='search_users'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
