from django.urls import path

from src.payment.views.online_payment import customer_payment_result

urlpatterns = [
    path('result/', customer_payment_result, name='customer-payment-result'),
]