from django.urls import path
from .views import PropertyListCreateView
from django.urls import path
from .views import(
    PropertyListCreateView,
    PropertyDetailView,
    api_root,
    home)

urlpatterns = [
    path('', home, name='home'),
    path('api/', api_root, name='api-root'),
    path('api/properties/', PropertyListCreateView.as_view(), name='property-list'),
    path('api/properties/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
   path('properties/', PropertyListCreateView.as_view(), name='property-list'),
]