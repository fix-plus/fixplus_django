import re

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from src.account.serializers.contact_number import OutPutContactNumberSerializer, InputContactNumbersSerializer
from src.customer.models import Customer


class InputCustomerSerializer(serializers.Serializer):
    customer_id = serializers.UUIDField(required=False, allow_null=True, default=None)
    full_name = serializers.CharField(required=True, max_length=200)
    gender = serializers.ChoiceField(choices=Customer.GENDER_CHOICES, required=True)
    contact_numbers = serializers.ListField(required=False, child=InputContactNumbersSerializer(), default=None)


class OutPutCustomerSerializer(serializers.ModelSerializer):
    searched_phone_number = serializers.CharField(required=False, default=None)
    contact_numbers = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['id', 'full_name', 'gender', 'searched_phone_number', 'contact_numbers']

    def get_contact_numbers(self, obj):
        return OutPutContactNumberSerializer(obj.contact_numbers, many=True).data


class OutPutPublicCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'full_name', 'gender',]


class InputCustomerParamsSerializer(serializers.Serializer):
    phone = serializers.CharField(required=False, default=None)
    full_name = serializers.CharField(required=False, default=None)
    sort_by = serializers.ChoiceField(required=False, default=None, choices=['created_at', 'updated_at'])
    order = serializers.CharField(required=False, default=None)

    def validate_phone(self, phone):
        if phone is None:
            return None

        # Regular expression to validate and format the mobile number
        pattern = r'^(00|\+)\d+$'

        if not re.match(pattern, phone):
            raise serializers.ValidationError({"detail": _("Mobile number must start with '00' or '+' and contain only digits after that.")})

        # Replace '00' with '+'
        if phone.startswith('00'):
            phone = '+' + phone[2:]

        return phone

