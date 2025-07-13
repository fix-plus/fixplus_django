from django.urls import path, include


urlpatterns = [
    path('account/', include('src.account.urls.technician')),
    path('geo/', include('src.geo.urls.technician')),
    path('service/', include('src.service.urls.technician')),
]