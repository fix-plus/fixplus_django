from rest_framework import serializers

from src.parametric.serializers.serializers import OutPutBrandNameParametricSerializer, \
    OutPutDeviceTypeParametricSerializer
from src.account.models import TechnicianSkill


class InputTechnicianSkillParamsSerializer(serializers.Serializer):
    device_type = serializers.CharField(required=False, allow_null=True, default=None)
    sort_by = serializers.ChoiceField(required=False, default=None, choices=['created_at', 'updated_at'])
    order = serializers.CharField(required=False, default=None)


class InputTechnicianSkillSerializer(serializers.Serializer):
    device_type = serializers.CharField(required=True)
    brand_names = serializers.ListField(required=True, child=serializers.CharField())


class InputUpdateTechnicianSkillSerializer(serializers.Serializer):
    device_type = serializers.CharField(required=False, allow_null=True, default=None)
    brand_names = serializers.ListField(required=False, allow_null=True, default=None, child=serializers.CharField())


class OutputTechnicianSkillSerializer(serializers.ModelSerializer):
    device_type = OutPutDeviceTypeParametricSerializer()
    brand_names = OutPutBrandNameParametricSerializer(many=True)

    class Meta:
        model = TechnicianSkill
        fields = ['id', 'device_type', 'brand_names']
