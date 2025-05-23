
from django.urls import path, include
from .views import (
    api_root,
    PublicPropertyListView,
    PropertyViewSet,
    rentke_view,
    home
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('properties', PropertyViewSet, basename='property')

app_name = 'listings'

urlpatterns = [
    
    path('', api_root, name='api-root'),
    path('listings/', include([
        path('', PublicPropertyListView.as_view(), name='listings-index'),
        path('public/', PublicPropertyListView.as_view(), name='public-listings'),
    # If you want to keep these separate from the ViewSet
    path('rentke/', rentke_view, name='rentke'),
    path('home/', home, name='home'),
    ])),
]

urlpatterns += router.urls