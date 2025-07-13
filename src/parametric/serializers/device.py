from rest_framework import serializers
from src.parametric.models import Brand, DeviceType, TimingSetting


class InputDeviceTypeParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ['title', 'fa_title', 'order',]


class OutPutDeviceTypeParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ['id', 'title', 'fa_title',]
