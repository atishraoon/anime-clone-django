from django.contrib import admin
from django.urls import path, include
from base import views

urlpatterns = [
    #all apps url
    path('', include('base.urls')),

    path('samriti/', admin.site.urls),
]

