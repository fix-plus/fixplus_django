from rest_framework import serializers

from src.customer.models import CustomerContactNumber


class InputContactNumbersSerializer(serializers.Serializer):
    phone_type = serializers.ChoiceField(required=True, choices=CustomerContactNumber.PhoneType.choices)
    is_primary = serializers.BooleanField(required=False, default=False)
    number = serializers.CharField(required=True)


class OutPutContactNumberSerializer(serializers.Serializer):
    phone_type = serializers.CharField()
    is_primary = serializers.BooleanField()
    number = serializers.CharField()
