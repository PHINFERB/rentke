from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home  # Home is project-wide

urlpatterns = [
    path('', home, name='home'),  # Project homepage
    path('', include('listings.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('listings.urls')),  # All API routes delegated
    path('rentke/', include('listings.urls')),  # All rentke routes delegated
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)