from django.urls import path
from .views import PropertyListCreateView
from django.urls import path
from .views import(
    PropertyListCreateView,
    PropertyDetailView,
    api_root,
    home)
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', home, name='home'),
    path('api/', api_root, name='api-root'),
    path('api/properties/', PropertyListCreateView.as_view(), name='property-list'),
    path('api/properties/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
   path('properties/', PropertyListCreateView.as_view(), name='property-list'),
path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),
]