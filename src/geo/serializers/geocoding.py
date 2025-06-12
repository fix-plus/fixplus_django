from rest_framework import serializers


class InputParamsGeoCodingSerializer(serializers.Serializer):
    address = serializers.CharField(required=True)


class OutputGeoCodingSerializer(serializers.Serializer):
    status = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    class Meta:
        fields = ['status', 'latitude', 'longitude']