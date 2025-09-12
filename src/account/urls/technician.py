from django.urls import path

from src.account.apis.technician.technician_own_service_card import TechnicianOwnServiceCardListApi
from src.account.apis.technician.technician_status import TechnicianStatusApi

urlpatterns = [
    path('me/status/', TechnicianStatusApi.as_view(), name="technician-status"),
    path('service-card/', TechnicianOwnServiceCardListApi.as_view(), name='technician-own-service-card-list'),
]
