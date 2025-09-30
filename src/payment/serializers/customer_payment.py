from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from azbankgateways.models import Bank

from src.payment.models import CustomerPayment


class InputCustomerPaymentSerializer(serializers.Serializer):
    service_id = serializers.UUIDField()
    cheque_amount = serializers.IntegerField(required=False, default=None)
    cash_amount = serializers.IntegerField(required=False, default=None)
    card_to_card_amount = serializers.IntegerField(required=False, default=None)
    online_amount = serializers.IntegerField(required=False, default=None)
    online_phone_number = serializers.CharField(max_length=15, required=False, default=None)

    def validate(self, attrs):
        # At least one payment amount must be provided
        if not any([
            attrs.get('cheque_amount'),
            attrs.get('cash_amount'),
            attrs.get('card_to_card_amount'),
            attrs.get('online_amount')
        ]):
            raise serializers.ValidationError(_("At least one payment amount must be provided."))

        # If online_amount is provided, online_phone_number must also be provided
        if attrs.get('online_amount') and not attrs.get('online_phone_number'):
            raise serializers.ValidationError(_("online_phone_number is required when online_amount is provided."))

        return attrs


class InputVerifyCustomerPaymentSerializer(serializers.Serializer):
    service_id = serializers.UUIDField(required=True)


class OutputCustomerPaymentSerializer(serializers.ModelSerializer):
    service_status = serializers.SerializerMethodField()
    class Meta:
        model = CustomerPayment
        fields = ['service_status', 'cheque_amount', 'cash_amount', 'card_to_card_amount', 'online_amount', 'online_phone_number',]

    def get_service_status(self, obj):
        return obj.service.status