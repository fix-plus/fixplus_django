from rest_framework import serializers


class InputAssignToTechnicianParamsSerializer(serializers.Serializer):
    technician_id = serializers.UUIDField(required=True)