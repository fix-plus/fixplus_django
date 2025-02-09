from django.urls import path

from src.account.apis.user.profile import ProfileApi
from src.account.apis.user.register import RegisterApi
from src.account.apis.user.users import UserListApi, UserDetailAPIView
from src.account.apis.user.skill import TechnicianSkillListApi, TechnicianSkillDetailApi

urlpatterns = [

    path('profile/', ProfileApi.as_view(), name="profile"),

    path('register/', RegisterApi.as_view(), name="register"),

    path('skill/', TechnicianSkillListApi.as_view(), name="skill-list"),
    path('skill/<uuid:uuid>/', TechnicianSkillDetailApi.as_view(), name="skill-detail"),

    path('', UserListApi.as_view(), name='account-list-create'),
    path('<uuid:uuid>/', UserDetailAPIView.as_view(), name='account-detail'),

]
