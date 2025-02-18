from rest_framework import serializers

from src.geo.models import Address


class OutPutAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address', 'latitude', 'longitude']