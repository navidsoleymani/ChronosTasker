from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from config.settings import (
    STATIC_URL,
    STATIC_ROOT,
    MEDIA_URL,
    MEDIA_ROOT,
)

schema_view = get_schema_view(
    openapi.Info(
        title="ChronosTasker APIs",
        default_version='v1',
        description="Designed for asynchronous and periodic task execution... .",
        contact=openapi.Contact(email="navidsoleymani@ymail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = (
        [
            path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
            path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
            path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
            path('api/v1/', include('config.interfaces.v1')),
        ]
        + i18n_patterns(path('admin/', admin.site.urls), )
        + static(STATIC_URL, document_root=STATIC_ROOT)
        + static(MEDIA_URL, document_root=MEDIA_ROOT)
)
admin.site.site_header = 'ChronosTasker'
admin.site.site_title = 'ChronosTasker.com'
admin.site.index_title = _('ChronosTasker Management Panel')
