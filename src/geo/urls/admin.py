from django.urls import path

from src.geo.apis.admin.geocoding import GeoCodingApi

urlpatterns = [
    path('geocoding/', GeoCodingApi.as_view(), name="geocoding"),
]
