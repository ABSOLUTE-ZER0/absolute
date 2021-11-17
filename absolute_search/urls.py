from django import urls
from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path("q=<query>&page=<page>&sort=<sort>", views.search_results, name='search_results'),
  path("q=<query>&page=<page>", views.search_results, name='search_results'),
  path("q=<query>", views.search_results, name='search_results'),
  path("doc/<index>/<id>", views.search_results, name='search_results'),
]