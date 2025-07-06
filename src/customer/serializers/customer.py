import re

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from src.account.serializers.contact_number import OutPutContactNumberSerializer, InputContactNumbersSerializer
from src.communication.selectors.customer_pin_message import get_latest_customer_pin_message
from src.communication.serializers.pin_message import PinMessageSerializer
from src.customer.models import Customer


class InputCustomerSerializer(serializers.Serializer):
    customer_id = serializers.UUIDField(required=False, allow_null=True, default=None)
    full_name = serializers.CharField(required=False, max_length=200, default=None)
    gender = serializers.ChoiceField(choices=Customer.Gender.choices, required=False, default=None)
    contact_numbers = serializers.ListField(required=False, child=InputContactNumbersSerializer(), default=None)
    pin_message = serializers.CharField(required=False, allow_blank=True, default=None)


class OutPutCustomerSerializer(serializers.ModelSerializer):
    searched_phone_number = serializers.CharField(required=False, default=None)
    contact_numbers = serializers.SerializerMethodField()
    pin_message = serializers.SerializerMethodField()
    in_processing_count = serializers.SerializerMethodField()
    canceled_count = serializers.SerializerMethodField()
    done_count = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['id', 'full_name', 'gender', 'searched_phone_number', 'contact_numbers', 'pin_message', 'in_processing_count', 'canceled_count', 'done_count']

    def get_contact_numbers(self, obj):
        return OutPutContactNumberSerializer(obj.contact_numbers, many=True).data

    def get_pin_message(self, obj):
        queryset = get_latest_customer_pin_message(customer=obj)
        return PinMessageSerializer(queryset).data if queryset else None

    def get_in_processing_count(self, obj):
        return  3

    def get_canceled_count(self, obj):
        return 1

    def get_done_count(self, obj):
        return 7


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
