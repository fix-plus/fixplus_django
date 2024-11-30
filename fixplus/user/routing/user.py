from django.urls import path

from fixplus.user.apis.user.profile import ProfileApi

urlpatterns = [
    path('profile/', ProfileApi.as_view(), name="profile"),
]
