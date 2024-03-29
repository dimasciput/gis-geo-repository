# coding=utf-8
"""Main django urls."""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'', include('dashboard.urls'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
