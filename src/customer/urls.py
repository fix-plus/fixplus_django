from django.urls import path

from src.customer.apis.customer import CustomerListApi, CustomerDetailApi

urlpatterns = [
    path('', CustomerListApi.as_view(), name='customer-list'),
    path('<uuid:customer_id>/', CustomerDetailApi.as_view(), name='customer-detail'),
]