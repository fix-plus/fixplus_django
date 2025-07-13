from django.urls import path

from src.service.apis.admin.assign_to_technician import AssignServiceToTechnicianApi
from src.service.apis.admin.service import AdminServiceListApi
from src.service.apis.admin.technician_for_service import TechnicianForServiceListApi

urlpatterns = [
    path('', AdminServiceListApi.as_view(), name='admin-service-list'),
    path('<uuid:uuid>/lookup-technician/', TechnicianForServiceListApi.as_view(), name='admin-technician-for-service'),
    path('<uuid:uuid>/assign-to-technician/', AssignServiceToTechnicianApi.as_view(), name='admin-assign-to-technician'),
]