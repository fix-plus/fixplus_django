from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from ceo.view import robots_txt

admin.site.site_header = "FixPlus Admin"
admin.site.site_title = "FixPlus Admin"
admin.site.index_title = "Panel v0.1"


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("schema/", SpectacularAPIView.as_view(api_version="v1"), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path('robots.txt', robots_txt),

    path('auth/', include('src.authentication.urls')),

    path('account/', include('src.account.urls')),

    path('media/', include('src.media.urls')),

    path('service/', include('src.service.urls')),

    path('customer/', include('src.customer.urls')),

    path('parametric/', include('src.parametric.urls')),

    path('geo/', include('src.geo.urls')),

    path('metric/', include('src.metric.urls')),
]
urlpatterns += i18n_patterns(
    path(_('admin/'), admin.site.urls),
)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)