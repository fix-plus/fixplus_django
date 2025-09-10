from django.urls import path

from src.account.apis.technician.technician_status import TechnicianStatusApi

urlpatterns = [
    path('me/status/', TechnicianStatusApi.as_view(), name="technician-status"),
]
