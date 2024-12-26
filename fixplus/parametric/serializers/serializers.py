from rest_framework import serializers
from fixplus.parametric.models import BrandNameParametric, DeviceTypeParametric, TimingSettingParametric


class InputBrandNameParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandNameParametric
        fields = ['title', 'fa_title', 'description', 'fa_description']


class OutPutBrandNameParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandNameParametric
        fields = ['id', 'title', 'fa_title', 'description', 'fa_description']


class InputDeviceTypeParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceTypeParametric
        fields = ['title', 'fa_title', 'description', 'fa_description']


class OutPutDeviceTypeParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceTypeParametric
        fields = ['id', 'title', 'fa_title', 'description', 'fa_description']


class InputTimingSettingParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimingSettingParametric
        fields = '__all__'


class OutPutTimingSettingParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimingSettingParametric
        fields = '__all__'