from django.urls import path

from src.payment.apis.customer_online_payment import CreateCustomerPaymentApi, VerifyCustomerPaymentApi
from src.payment.apis.technician_online_payment import InitiateTechnicianOnlinePaymentApi
from src.payment.views.online_payment import payment_callback, technician_payment_result

urlpatterns = [
    path('service/', CreateCustomerPaymentApi.as_view(), name='create-customer-payment'),
    path('internal-wallet/initiate/', InitiateTechnicianOnlinePaymentApi.as_view(), name='technician-online-payment-initiate'),
    path('service/verify/', VerifyCustomerPaymentApi.as_view(), name='verify-customer-payment'),
    path('callback-gateway/', payment_callback, name='callback-gateway'),
    path('result/', technician_payment_result, name='technician-payment-result'),
]