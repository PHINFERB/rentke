from django.urls import path
from .views import PropertyListCreateView
from .views import(PropertyListCreateView,PropertyDetailView,api_root,home, rentke_view)
from .views import PublicPropertyListView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (PropertyListCreateView,PropertyDetailView,UserPropertiesView,SearchPropertiesView,api_root,home,rentke_view)

urlpatterns = [
   #Basic views
    path('', home, name='home'),
    path('api/', api_root, name='api-root'),
    path('rentke/', rentke_view, name='rentke'),
    
    # API views for properties
    path('public/', PublicPropertyListView.as_view(), name='public-listings'),
    path('properties/', PropertyListCreateView.as_view(), name='property-list'),
    path('properties/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),

   # Redirect for favicon
    # This assumes you have a favicon.ico in your static files under img/
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),
    path('properties/user/', UserPropertiesView.as_view(), name='user-properties'),
    path('properties/search/', SearchPropertiesView.as_view(), name='property-search'),
    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Schema (OpenAPI JSON)
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc')
]