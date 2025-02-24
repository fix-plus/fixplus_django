from django.urls import path

from src.service.apis.service import ServiceListApi

urlpatterns = [
    path('', ServiceListApi.as_view(), name='service-list'),
]