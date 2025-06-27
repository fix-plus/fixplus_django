from rest_framework import serializers


class OutputAdminPinMessageOfTechnicianSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField()
