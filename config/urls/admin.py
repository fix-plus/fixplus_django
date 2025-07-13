from django.urls import path, include


urlpatterns = [
    path('service/', include('src.service.urls.admin')),
    path('customer/', include('src.customer.urls.admin')),
    path('account/', include('src.account.urls.admin')),
    path('parametric/', include('src.parametric.urls.admin')),
    path('geo/', include('src.geo.urls.admin')),
    path('metric/', include('src.metric.urls.admin')),
]