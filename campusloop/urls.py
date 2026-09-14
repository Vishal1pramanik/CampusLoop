from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView

from core.views import (
    home,
    listings,
    add_listing,
    listing_detail,
    register,
    contact_seller,
    inbox,
    conversation,
    logout_user,
    dashboard,
    my_requests,
    mark_as_sold,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path('listings/', listings, name='listings'),

    path('add/', add_listing, name='add_listing'),

    path(
        'listings/<int:id>/',
        listing_detail,
        name='listing_detail'
    ),

    path('register/', register, name='register'),

    path(
        'login/',
        LoginView.as_view(
            template_name='core/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        logout_user,
        name='logout'
    ),

    path(
        'listings/<int:id>/contact/',
        contact_seller,
        name='contact_seller'
    ),

    path(
        'inbox/',
        inbox,
        name='inbox'
    ),

    path(
        'listings/<int:id>/conversation/<int:user_id>/',
        conversation,
        name='conversation'
    ),

    path(
        'listings/<int:id>/mark-sold/',
        mark_as_sold,
        name='mark_as_sold'
    ),

    path(
        'dashboard/',
        dashboard,
        name='dashboard'
    ),

    path(
        'my-requests/',
        my_requests,
        name='my_requests'
    ),
]