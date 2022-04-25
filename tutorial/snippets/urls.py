from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('UserChangePassword/', UserProfileView.as_view(), name='change'),
    path('CreateList', CRUDView.as_view(), name='createlist'),
    path('DeleteList/<int:instance>', CRUDView.as_view(), name='delete list'),
    path('UpdatedList/<int:instance>', CRUDView.as_view(), name='edit-list'),
    path('List/', CRUDView.as_view(), name='realist'),
    path('List/Filtered', Filtering.as_view(), name='filtering'),
    path('searching', Searching.as_view(), name='searching'),
    path('Image', ImageUpload.as_view(), name='Image_upload')
    # path('List/search/', SEARCHAPIView.as_view(), name='searching')

]

