from django.urls import path
from src.payment.apis.customer_online_payment import InitiateCustomerOnlinePaymentApi
from src.payment.views.online_payment import payment_callback, technician_payment_result, customer_payment_result

urlpatterns = [
    path('online/result/', customer_payment_result, name='customer-payment-result'),
]