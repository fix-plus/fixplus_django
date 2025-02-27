from rest_framework import serializers


class PinMessageSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    is_seen = serializers.BooleanField()
    is_read = serializers.BooleanField()
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField()
