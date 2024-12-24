from django.urls import path

from fixplus.customer.apis.customer import CustomerListApi

urlpatterns = [
    path('', CustomerListApi.as_view(), name='customer-list'),
]
