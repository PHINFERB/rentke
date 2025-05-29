from django.urls import path
from .views import PropertyListCreateView
from .views import(PropertyListCreateView,PropertyDetailView,api_root,home, rentke_view)
from .views import PublicPropertyListView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('', home, name='home'),
    path('api/', api_root, name='api-root'),
    path('rentke/', rentke_view, name='rentke'),
    path('api/properties/', PropertyListCreateView.as_view(), name='property-list'),
    path('api/properties/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
    path('api/public/', PublicPropertyListView.as_view(), name='public-listings'),
    path('properties/', PropertyListCreateView.as_view(), name='property-list'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),

   # Schema (OpenAPI JSON)
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc')
]