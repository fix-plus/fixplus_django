from rest_framework import serializers

from src.account.models import TechnicianServiceZone


class InputTechnicianServiceZoneParamsSerializer(serializers.Serializer):
    sort_by = serializers.ChoiceField(required=False, default=None, choices=['created_at', 'updated_at'])
    order = serializers.CharField(required=False, default=None)


class InputTechnicianServiceZoneSerializer(serializers.Serializer):
    zone = serializers.CharField(required=True, max_length=50)



class InputUpdateTechnicianServiceZoneSerializer(serializers.Serializer):
    zone = serializers.CharField(required=False, allow_null=True, default=None)


class OutputTechnicianServiceZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicianServiceZone
        fields = ['id', 'zone']
