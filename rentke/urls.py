from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home  # Home is project-wide
from drf_spectacular.views import (SpectacularAPIView,SpectacularSwaggerView,SpectacularRedocView)

urlpatterns = [
    # Basic views
    # Home view for the project
    path('', home, name='home'),  # Project homepage
    # API root view
    path('admin/', admin.site.urls),
    # API routes for the listings app
    path('api/', include('listings.urls')),  # All API routes delegated to listings.urls
    #API schema generation and documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)