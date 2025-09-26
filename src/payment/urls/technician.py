from django.urls import path
from src.payment.apis.customer_online_payment import InitiateCustomerOnlinePaymentApi
from src.payment.views.online_payment import payment_callback, technician_payment_result

urlpatterns = [
    path('online/service/initiate/', InitiateCustomerOnlinePaymentApi.as_view(), name='payment-initiate'),
    path('online/callback-gateway/', payment_callback, name='callback-gateway'),
    path('online/result/', technician_payment_result, name='technician-payment-result'),
]