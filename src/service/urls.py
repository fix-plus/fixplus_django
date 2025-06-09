from django.urls import path

from src.service.apis.assign_to_technician import AssignServiceToTechnicianApi
from src.service.apis.service import ServiceListApi
from src.service.apis.technician_for_service import TechnicianForServiceListApi

urlpatterns = [
    path('', ServiceListApi.as_view(), name='service-list'),
    path('<uuid:uuid>/lookup-technician/', TechnicianForServiceListApi.as_view(), name='technician-for-service'),
    path('<uuid:uuid>/assign-to-technician/', AssignServiceToTechnicianApi.as_view(), name='assign-to-technician'),
]