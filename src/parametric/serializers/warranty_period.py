from rest_framework import serializers
from src.parametric.models import WarrantyPeriod


class InputWarrantyPeriodParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarrantyPeriod
        fields = ['time_unit', 'duration',]


class OutPutWarrantyPeriodParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarrantyPeriod
        fields = ['id', 'time_unit', 'duration', 'duration_in_days']