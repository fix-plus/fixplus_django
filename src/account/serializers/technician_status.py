from rest_framework import serializers

from src.account.models import TechnicianStatus


class InputTechnicianStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=TechnicianStatus.Status.choices, required=True)


class OutputTechnicianStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicianStatus
        fields = ['status', 'created_at']
