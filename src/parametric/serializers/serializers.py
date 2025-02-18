from rest_framework import serializers
from src.parametric.models import Brand, DeviceType, TimingSetting


class InputBrandNameParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['title', 'fa_title', 'order',]


class OutPutBrandNameParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title', 'fa_title',]


class InputDeviceTypeParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ['title', 'fa_title', 'order',]


class OutPutDeviceTypeParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ['id', 'title', 'fa_title',]


class InputTimingSettingParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimingSetting
        fields = '__all__'


class OutPutTimingSettingParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimingSetting
        fields = '__all__'