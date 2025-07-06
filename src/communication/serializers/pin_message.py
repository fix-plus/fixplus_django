from rest_framework import serializers


class PinMessageSerializer(serializers.Serializer):
    description = serializers.CharField()
    created_at = serializers.DateTimeField()
