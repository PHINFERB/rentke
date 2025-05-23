from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# Swagger Configuration
schema_view = get_schema_view(
    openapi.Info(
        title="RentKe API",
        default_version="v1",
        description="API documentation for RentKe Property Listings",
        contact=openapi.Contact(email="your@email.com"),
    ),
    public=True,
)

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('', home, name='home'),  # Project homepage
    path('', include('listings.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('listings.urls')),  # All API routes delegated
    path('rentke/', include('listings.urls')),  # All rentke routes delegated
    # Swagger URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)