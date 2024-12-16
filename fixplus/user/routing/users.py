from django.urls import path

from fixplus.user.apis.user.group import AssignGroupAPIView
from fixplus.user.apis.user.permission import AssignPermissionAPIView
from fixplus.user.apis.user.profile import ProfileApi
from fixplus.user.apis.user.register import RegisterApi
from fixplus.user.apis.user.users import UserListApi, UserDetailAPIView

urlpatterns = [
    path('permissions/', AssignPermissionAPIView.as_view(), name='assign-permission'),

    path('profile/', ProfileApi.as_view(), name="profile"),

    path('register/', RegisterApi.as_view(), name="register"),

    path('', UserListApi.as_view(), name='user-list-create'),
    path('<uuid:uuid>/', UserDetailAPIView.as_view(), name='user-detail'),

    path('<uuid:user_id>/groups/', AssignGroupAPIView.as_view(), name='assign-group'),
]
