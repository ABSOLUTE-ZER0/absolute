from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('absolute_search.urls')),
    path('/', include('absolute_search.urls')),
]
 