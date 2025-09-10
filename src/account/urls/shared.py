from django.urls import path

from src.account.apis.shared.me import MeApi
from src.account.apis.shared.register import RegisterApi

urlpatterns = [
    path('me/', MeApi.as_view(), name="me"),
    path('register/', RegisterApi.as_view(), name="register"),
]
