from rest_framework import serializers
from azbankgateways.models import Bank


class InputInitiateCustomerOnlinePaymentSerializer(serializers.Serializer):
    service_id = serializers.UUIDField()
    amount = serializers.IntegerField()
    customer_phone_number = serializers.CharField(max_length=15)


class OutputPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = (
            'id',
            'amount',
            'tracking_code',
            'status',
            'created_at',
        )