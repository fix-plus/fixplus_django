from django.urls import path

from src.account.apis.me import MeApi
from src.account.apis.register import RegisterApi
from src.account.apis.technician_service_card import TechnicianServiceCardListApi, TechnicianServiceCardDetailApi
from src.account.apis.technician_service_zone import TechnicianServiceZoneListApi, TechnicianServiceZoneDetailApi
from src.account.apis.technician_status import TechnicianStatusApi
from src.account.apis.users import UsersListApi, UserDetailAPIView
from src.account.apis.technician_skill import TechnicianSkillListApi, TechnicianSkillDetailApi

urlpatterns = [

    path('me/', MeApi.as_view(), name="me"),
    path('me/technician-status/', TechnicianStatusApi.as_view(), name="technician-status"),

    path('register/', RegisterApi.as_view(), name="register"),

    path('users/', UsersListApi.as_view(), name='account-list-create'),
    path('users/<uuid:uuid>/', UserDetailAPIView.as_view(), name='account-detail'),

    path('users/<uuid:uuid>/skill/', TechnicianSkillListApi.as_view(), name='skill-list'),
    path('users/skill/<uuid:skill_id>/', TechnicianSkillDetailApi.as_view(), name='skill-detail'),

    path('users/<uuid:uuid>/service-zone/', TechnicianServiceZoneListApi.as_view(), name='service-zone-list'),
    path('users/service-zone/<uuid:service_zone_id>/', TechnicianServiceZoneDetailApi.as_view(), name='service-zone-detail'),

    path('users/<uuid:technician_id>/service-card/', TechnicianServiceCardListApi.as_view(), name='service-card-list'),
    path('users/service-card/<uuid:service_card_id>/', TechnicianServiceCardDetailApi.as_view(), name='service-card-detail'),
]
