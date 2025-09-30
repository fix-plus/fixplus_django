from django.urls import path

from src.service.apis.technician.accept_service import TechnicianAcceptServiceApi
from src.service.apis.technician.customer_invoice_service import CustomerInvoiceServiceApi
from src.service.apis.technician.customer_service_signature import CustomerServiceSignatureApi
from src.service.apis.technician.service import TechnicianServiceListApi, TechnicianServiceDetailApi

urlpatterns = [
    path('', TechnicianServiceListApi.as_view(), name='technician-service-list'),
    path('<uuid:service_id>/accept/', TechnicianAcceptServiceApi.as_view(), name='technician-accept-service'),
    path('<uuid:service_id>/customer-invoicing/', CustomerInvoiceServiceApi.as_view(), name='customer-invoice-service'),
    path('<uuid:service_id>/customer-signature/', CustomerServiceSignatureApi.as_view(), name='customer-service-signature'),
    path('<uuid:service_id>/', TechnicianServiceDetailApi.as_view(), name='technician-service-detail'),
]