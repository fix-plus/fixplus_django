from django.urls import path

from src.service.apis.technician.accept_service import TechnicianAcceptServiceApi
from src.service.apis.technician.service import TechnicianServiceListApi

urlpatterns = [
    path('', TechnicianServiceListApi.as_view(), name='technician-service-list'),
    path('<uuid:service_id>/accept/', TechnicianAcceptServiceApi.as_view(), name='technician-accept-service'),
]