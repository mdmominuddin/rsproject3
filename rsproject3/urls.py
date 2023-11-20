from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static  # Import for serving media files


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('django.contrib.auth.urls', 'auth'))),
    path('', include('myapp.urls')),
]

if settings.DBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Add for serving media files during development
