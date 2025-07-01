from rest_framework import serializers


class OutputAdminPinMessageOfTechnicianSerializer(serializers.Serializer):
    description = serializers.CharField()
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField()
