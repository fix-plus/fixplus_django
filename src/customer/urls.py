from django.urls import path

from src.customer.apis.customer import CustomerListApi

urlpatterns = [
    path('', CustomerListApi.as_view(), name='customer-list'),
]