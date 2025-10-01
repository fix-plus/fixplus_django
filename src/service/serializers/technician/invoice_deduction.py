from rest_framework import serializers


class InputInvoiceDeductionItemSerializer(serializers.Serializer):
    description = serializers.CharField(required=True)
    cost = serializers.IntegerField(required=True, min_value=0)
    quantity = serializers.IntegerField(required=True, min_value=1)


class InputInvoiceDeductionSerializer(serializers.Serializer):
    ignored_system_fee = serializers.BooleanField(required=False, default=None)
    deduction_items = InputInvoiceDeductionItemSerializer(many=True, required=False, default=None)
    other_invoice_deduction_description = serializers.CharField(required=False, allow_null=True, default=None)

    def validate(self, data):
        # Ensure ignored_system_fee is False or deduction_items not empty
        if not data.get('ignored_system_fee') and not data.get('deduction_items'):
            raise serializers.ValidationError("Either 'ignored_system_fee' must be True or 'deduction_items' must be provided.")
        return data

