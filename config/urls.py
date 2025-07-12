from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
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

# Swagger/OpenAPI schema configuration
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

# Main URL patterns
urlpatterns = (
    [
        # Swagger schema in JSON or YAML format
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),

        # Swagger UI documentation
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

        # ReDoc documentation UI
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

        # API version 1 interface
        path('api/v1/', include('config.interfaces.v1')),
    ]

    # Admin panel with language internationalization support
    + i18n_patterns(
        path('admin/', admin.site.urls),
    )

    # Static and media files configuration
    + static(STATIC_URL, document_root=STATIC_ROOT)
    + static(MEDIA_URL, document_root=MEDIA_ROOT)
)

# Admin site branding and titles (supports i18n)
admin.site.site_header = 'ChronosTasker'
admin.site.site_title = 'ChronosTasker.com'
admin.site.index_title = _('ChronosTasker Management Panel')
