from django.urls import path

from src.geo.apis.geocoding import GeoCodingApi
from src.geo.apis.user_location_tracker import UserLocationTrackerApi


urlpatterns = [
    path('location-tracker/', UserLocationTrackerApi.as_view(), name="location_tracker"),
    path('geocoding/', GeoCodingApi.as_view(), name="geocoding"),
]
