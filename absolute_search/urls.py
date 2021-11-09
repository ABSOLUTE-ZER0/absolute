from django import urls
from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path(r"q=<query>", views.search_results, name='search_results'),
]