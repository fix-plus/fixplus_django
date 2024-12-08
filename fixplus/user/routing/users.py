from django.urls import path

from fixplus.user.apis.user.group import AssignGroupAPIView
from fixplus.user.apis.user.permission import AssignPermissionAPIView
from fixplus.user.apis.user.profile import ProfileApi
from fixplus.user.apis.user.users import UserListCreateAPIView, UserDetailAPIView

urlpatterns = [
    # User Management
    path('', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('<uuid:pk>/', UserDetailAPIView.as_view(), name='user-detail'),

    # Group Assignment
    path('<uuid:user_id>/groups/', AssignGroupAPIView.as_view(), name='assign-group'),

    # Permission Assignment
    path('permissions/', AssignPermissionAPIView.as_view(), name='assign-permission'),

    path('profile/', ProfileApi.as_view(), name="profile"),
]
