from rest_framework import serializers

from fixplus.parametric.serializers.serializers import OutPutBrandNameParametricSerializer, \
    OutPutDeviceTypeParametricSerializer
from fixplus.user.models import TechnicianSkill


class InputTechnicianSkillParamsSerializer(serializers.Serializer):
    technician_id = serializers.UUIDField(required=True)
    device_type = serializers.CharField(required=False, allow_null=True, default=None)


class InputTechnicianSkillSerializer(serializers.Serializer):
    technician_id = serializers.UUIDField(required=True)
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
