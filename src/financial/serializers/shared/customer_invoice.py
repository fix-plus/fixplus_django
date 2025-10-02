from rest_framework import serializers

from src.parametric.serializers.warranty_period import OutPutWarrantyPeriodParametricSerializer


class OutPutCustomerInvoiceSerializer(serializers.Serializer):
    warranty_period = OutPutWarrantyPeriodParametricSerializer()
    warranty_description = serializers.CharField()
    discount_amount = serializers.IntegerField()
    wage_cost = serializers.IntegerField()
    deadheading_cost = serializers.IntegerField()
    pdf_output = serializers.FileField()