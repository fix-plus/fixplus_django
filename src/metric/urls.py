from django.urls import path

from src.metric.apis.admin_dashboard import AdminDashboardMetricApi

urlpatterns = [
    path('admin-dashboard/', AdminDashboardMetricApi.as_view(), name="admin-dashboard"),
]
