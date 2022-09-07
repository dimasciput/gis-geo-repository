# coding=utf-8
"""Main django urls."""
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.urls import re_path, include, path
from django.conf.urls.static import static
from django.contrib import admin


schema_view = get_schema_view(
    openapi.Info(
        title="GeoRepo API",
        default_version='v0.1.0',
        description="GeoRepo API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    patterns=[
        re_path(r'', include(('georepo.urls', 'api'), namespace='api'))
    ],
)

admin.autodiscover()

urlpatterns = [
    path('account/', include('django.contrib.auth.urls')),
    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^auth/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r'', include('georepo.urls')),
    re_path(r'', include('dashboard.urls'))
]
