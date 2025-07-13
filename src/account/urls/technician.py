from django.urls import path

from src.account.apis.me import MeApi
from src.account.apis.register import RegisterApi
from src.account.apis.technician_service_card import TechnicianServiceCardListApi, TechnicianServiceCardDetailApi
from src.account.apis.technician_service_zone import TechnicianServiceZoneListApi, TechnicianServiceZoneDetailApi
from src.account.apis.technician_status import TechnicianStatusApi
from src.account.apis.users import UsersListApi, UserDetailAPIView
from src.account.apis.technician_skill import TechnicianSkillListApi, TechnicianSkillDetailApi

urlpatterns = [
    path('me/status/', TechnicianStatusApi.as_view(), name="technician-status"),
]
