from rest_framework import serializers
from src.parametric.models import Brand, DeviceType, TimingSetting


class InputBrandNameParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['title', 'fa_title', 'description', 'fa_description']


class OutPutBrandNameParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title', 'fa_title', 'description', 'fa_description']


class InputDeviceTypeParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ['title', 'fa_title', 'description', 'fa_description']


class OutPutDeviceTypeParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ['id', 'title', 'fa_title', 'description', 'fa_description']


class InputTimingSettingParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimingSetting
        fields = '__all__'


class OutPutTimingSettingParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimingSetting
        fields = '__all__'