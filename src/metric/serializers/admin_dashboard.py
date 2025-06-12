from rest_framework import serializers


class OutputAdminDashboardMetricSerializer(serializers.Serializer):
    awaiting_services_count = serializers.IntegerField()
    available_technicians_count = serializers.IntegerField()
    processing_services_count = serializers.IntegerField()
    withdrawal_requests_count = serializers.IntegerField()
