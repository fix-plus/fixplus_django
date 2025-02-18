from rest_framework import serializers


class InputContactNumbersSerializer(serializers.Serializer):
    phone_type = serializers.ChoiceField(required=True, choices=['mobile', 'landline'])
    is_primary = serializers.BooleanField(required=False, default=False)
    number = serializers.CharField(required=True)


class OutPutContactNumberSerializer(serializers.Serializer):
    phone_type = serializers.CharField()
    is_primary = serializers.BooleanField()
    number = serializers.CharField()
