from rest_framework import serializers
from azbankgateways.models import Bank


class InputInitiateTechnicianOnlinePaymentSerializer(serializers.Serializer):
    amount = serializers.IntegerField()


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