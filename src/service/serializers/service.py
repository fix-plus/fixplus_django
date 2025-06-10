import re

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from src.account.serializers.profile import OutPutProfileSerializer
from src.customer.serializers.customer import OutPutCustomerSerializer, OutPutPublicCustomerSerializer, \
    InputCustomerSerializer
from src.geo.serializers.address import OutPutAddressSerializer
from src.parametric.serializers.serializers import OutPutBrandNameParametricSerializer, \
    OutPutDeviceTypeParametricSerializer
from src.service.models import Service, ServiceHistory


class OutPutServiceSerializer(serializers.ModelSerializer):
    customer = OutPutCustomerSerializer()
    brand = OutPutBrandNameParametricSerializer()
    device_type = OutPutDeviceTypeParametricSerializer()
    address = OutPutAddressSerializer()
    technician = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    assigned_by = serializers.SerializerMethodField()
    assigned_at = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id',
            'device_type',
            'brand',
            'customer_description',
            'description_for_technician',
            'address',
            'status',
            'customer',
            'technician',
            'created_by',
            'assigned_by',
            'assigned_at',
            'created_at',
        ]

    def get_technician(self, obj):
        try:
            return OutPutProfileSerializer(obj.technician.profile, user_type='public').data
        except:
            return None

    def get_created_by(self, obj):
        try:
            return OutPutProfileSerializer(obj.created_by.profile, user_type='public').data
        except:
            return None

    def get_assigned_by(self, obj):
        try:
            queryset = obj.histories.filter(new_status=Service.Status.ASSIGNED).latest('created_at').created_by
            return OutPutProfileSerializer(queryset.profile, user_type='public').data
        except ServiceHistory.DoesNotExist:
            return None

    def get_assigned_at(self, obj):
        try:
            queryset = obj.histories.filter(new_status=Service.Status.ASSIGNED).latest('created_at').created_at
            return queryset
        except ServiceHistory.DoesNotExist:
            return None


class OutPutPublicServiceSerializer(serializers.ModelSerializer):
    customer = OutPutPublicCustomerSerializer()
    brand = OutPutBrandNameParametricSerializer()
    device_type = OutPutDeviceTypeParametricSerializer()

    class Meta:
        model = Service
        fields = ['id', 'device_type', 'brand', 'customer_description', 'description_for_technician', 'address', 'customer',]


class InputDeviceSerializer(serializers.Serializer):
    device_type = serializers.CharField(required=True)
    brand = serializers.CharField(required=True)
    customer_description = serializers.CharField(required=False, allow_blank=True)
    description_for_technician = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=True)


class InputServiceSerializer(serializers.Serializer):
    customer_data = InputCustomerSerializer(required=True)
    devices_data = InputDeviceSerializer(many=True, required=True)


class InputServiceParamsSerializer(serializers.Serializer):
    customer_name = serializers.CharField(required=False, default=None)
    customer_phone_number = serializers.CharField(required=False, default=None)
    device_type = serializers.CharField(required=False, default=None)
    brand = serializers.CharField(required=False, default=None)
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