from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class InputCompletedServiceItemSerializer(serializers.Serializer):
    description = serializers.CharField(required=True)
    cost = serializers.IntegerField(required=True, min_value=0)
    quantity = serializers.IntegerField(required=True, min_value=1)


class InputCustomerInvoiceServiceSerializer(serializers.Serializer):
    completed_service_items = InputCompletedServiceItemSerializer(many=True, required=False)
    discount_amount = serializers.IntegerField(required=False, min_value=0, default=0)
    warranty_period_id = serializers.UUIDField(required=False, allow_null=True, default=None)
    warranty_description = serializers.CharField(required=False, allow_null=True, default=None)
    wage_cost = serializers.IntegerField(required=False, min_value=0, default=0)
    deadheading_cost = serializers.IntegerField(required=False, min_value=0, default=0)

