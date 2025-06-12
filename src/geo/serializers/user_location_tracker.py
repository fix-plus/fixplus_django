from rest_framework import serializers


class InputUserLocationTrackerSerializer(serializers.Serializer):
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)


class OutputUserLocationTrackerSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    created_at = serializers.DateTimeField()

    class Meta:
        fields = ['latitude', 'longitude', 'created_at']