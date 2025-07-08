from rest_framework import serializers

from src.media.serializers import OutputMediaSerializer
from src.parametric.serializers.serializers import OutPutBrandNameParametricSerializer, \
    OutPutDeviceTypeParametricSerializer
from src.account.models import TechnicianServiceCard


class InputTechnicianServiceCardParamsSerializer(serializers.Serializer):
    brands = serializers.ListField(required=False, allow_null=True, default=None, child=serializers.CharField())
    sort_by = serializers.ChoiceField(required=False, default=None, choices=['created_at', 'updated_at'])
    order = serializers.CharField(required=False, default=None)


class InputTechnicianServiceCardSerializer(serializers.Serializer):
    brand = serializers.CharField(required=True)
    photo = serializers.UUIDField(required=True)


class InputUpdateTechnicianServiceCardSerializer(serializers.Serializer):
    brand = serializers.CharField(required=False, allow_null=True, default=None)
    photo = serializers.UUIDField(required=False, allow_null=True, default=None)


class OutputTechnicianServiceCardSerializer(serializers.ModelSerializer):
    brand = OutPutBrandNameParametricSerializer()
    photo = OutputMediaSerializer()

    class Meta:
        model = TechnicianServiceCard
        fields = ['id', 'brand', 'photo']
