import re

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from fixplus.customer.serializers.serializers import OutPutCustomerSerializer, InputCustomerSerializer, \
    OutPutPublicCustomerSerializer
from fixplus.job.models import Job
from fixplus.parametric.serializers.serializers import OutPutBrandNameParametricSerializer, \
    OutPutDeviceTypeParametricSerializer


class OutPutJobSerializer(serializers.ModelSerializer):
    customer = OutPutCustomerSerializer()
    brand_name = OutPutBrandNameParametricSerializer()
    device_type = OutPutDeviceTypeParametricSerializer()

    class Meta:
        model = Job
        fields = ['id', 'device_type', 'brand_name', 'customer_description', 'description_for_technician', 'address', 'status', 'customer', 'created_at', 'updated_at']


class OutPutPublicJobSerializer(serializers.ModelSerializer):
    customer = OutPutPublicCustomerSerializer()
    brand_name = OutPutBrandNameParametricSerializer()
    device_type = OutPutDeviceTypeParametricSerializer()

    class Meta:
        model = Job
        fields = ['id', 'device_type', 'brand_name', 'customer_description', 'description_for_technician', 'address', 'customer',]


class InputDeviceSerializer(serializers.Serializer):
    device_type = serializers.CharField(required=True)
    brand_name = serializers.CharField(required=True)
    customer_description = serializers.CharField(required=False, allow_blank=True)
    description_for_technician = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=True)


class InputJobSerializer(serializers.Serializer):
    customer_data = InputCustomerSerializer(required=True)
    devices_data = InputDeviceSerializer(many=True, required=True)


class InputJobParamsSerializer(serializers.Serializer):
    customer_name = serializers.CharField(required=False, default=None)
    customer_phone_number = serializers.CharField(required=False, default=None)
    device_type = serializers.CharField(required=False, default=None)
    brand_name = serializers.CharField(required=False, default=None)
    status = serializers.CharField(required=False, default=None)
    address = serializers.CharField(required=False, default=None)
    sort_by = serializers.ChoiceField(required=False, default=None, choices=['created_at', 'updated_at'])
    order = serializers.ChoiceField(required=False, default='desc', choices=['asc', 'desc'])

    def validate_customer_phone_number(self, phone_number):
        if phone_number is None:
            return None

        # Regular expression to validate and format the phone number
        pattern = r'^(00|\+)?\d+$'

        if not re.match(pattern, phone_number):
            raise serializers.ValidationError({"detail": _("Phone number must start with '00' or '+' and contain only digits after that.")})

        # Replace '00' with '+' if necessary
        if phone_number.startswith('00'):
            phone_number = '+' + phone_number[2:]

        return phone_number
