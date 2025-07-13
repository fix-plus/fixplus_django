from rest_framework import serializers
from src.parametric.models import Brand, DeviceType, TimingSetting


class InputTimingSettingParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimingSetting
        fields = '__all__'


class OutPutTimingSettingParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimingSetting
        fields = '__all__'