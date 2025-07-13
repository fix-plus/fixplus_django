from django.urls import path, include


urlpatterns = [
    path('auth/', include('src.authentication.urls.shared')),
    path('account/', include('src.account.urls.shared')),
    path('media/', include('src.media.urls.shared')),
    path('parametric/', include('src.parametric.urls.shared')),
]