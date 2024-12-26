from django.urls import path

from fixplus.user.apis.user.group import AssignGroupAPIView
from fixplus.user.apis.user.permission import AssignPermissionAPIView
from fixplus.user.apis.user.profile import ProfileApi
from fixplus.user.apis.user.register import RegisterApi
from fixplus.user.apis.user.users import UserListApi, UserDetailAPIView
from fixplus.user.apis.user.skill import TechnicianSkillListApi, TechnicianSkillDetailApi

urlpatterns = [
    path('permissions/', AssignPermissionAPIView.as_view(), name='assign-permission'),

    path('profile/', ProfileApi.as_view(), name="profile"),

    path('register/', RegisterApi.as_view(), name="register"),

    path('skill/', TechnicianSkillListApi.as_view(), name="skill-list"),
    path('skill/<uuid:uuid>/', TechnicianSkillDetailApi.as_view(), name="skill-detail"),

    path('', UserListApi.as_view(), name='user-list-create'),
    path('<uuid:uuid>/', UserDetailAPIView.as_view(), name='user-detail'),

    path('<uuid:user_id>/groups/', AssignGroupAPIView.as_view(), name='assign-group'),
]
