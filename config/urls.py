from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from config.settings import (
    STATIC_URL,
    STATIC_ROOT,
    MEDIA_URL,
    MEDIA_ROOT,
)

urlpatterns = (
        [
            path('api/v1/', include('config.interfaces.v1')),
        ]
        + i18n_patterns(path('admin/', admin.site.urls), )
        + static(STATIC_URL, document_root=STATIC_ROOT)
        + static(MEDIA_URL, document_root=MEDIA_ROOT)
)
admin.site.site_header = 'ChronosTasker'
admin.site.site_title = 'ChronosTasker.com'
admin.site.index_title = _('ChronosTasker Management Panel')
