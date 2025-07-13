from django.urls import path

from src.geo.apis.technician.user_location_tracker import UserLocationTrackerApi


urlpatterns = [
    path('location-tracker/', UserLocationTrackerApi.as_view(), name="location_tracker"),
]
