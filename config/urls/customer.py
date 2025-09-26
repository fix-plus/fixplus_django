from django.urls import path, include


urlpatterns = [
    path('payment/', include('src.payment.urls.customer')),
]