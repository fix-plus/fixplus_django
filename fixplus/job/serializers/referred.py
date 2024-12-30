import re

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from fixplus.job.models import ReferredJob
from fixplus.job.serializers.job import OutPutJobSerializer, OutPutPublicJobSerializer
from fixplus.user.serializers.user import OutPutSuperAdminUserDetailSerializer, OutPutPublicUserDetailSerializer, \
    OutPutAdminUserDetailSerializer


class InputReferredJobToTechnicianSerializer(serializers.Serializer):
    job_id = serializers.UUIDField(required=True)
    technician_id = serializers.UUIDField(required=True)


class OutPutAdminReferredJobSerializer(serializers.ModelSerializer):
    technician = OutPutAdminUserDetailSerializer()
    referred_by = OutPutAdminUserDetailSerializer()
    updated_by = OutPutAdminUserDetailSerializer()
    job = OutPutJobSerializer()

    class Meta:
        model = ReferredJob
        fields = [
            'id',
            'status',
            'job',
            'technician',
            'referred_by',
            'updated_by',
            'referred_at',
            'deadline_determine_at',
            'estimated_arrival_at',
            'determined_by_technician_at',
            'rejected_reason_by_technician',
        ]


class OutPutTechnicianReferredJobSerializer(serializers.ModelSerializer):
    referred_by = OutPutPublicUserDetailSerializer()
    job = serializers.SerializerMethodField()

    class Meta:
        model = ReferredJob
        fields = [
            'id',
            'status',
            'job',
            'referred_by',
            'referred_at',
            'deadline_determine_at',
            'estimated_arrival_at',
            'determined_by_technician_at',
            'rejected_reason_by_technician',
        ]

    def get_job(self, obj):
        if obj.status == 'in_processing':
            return OutPutJobSerializer(obj.job).data

        else:
            return OutPutPublicJobSerializer(obj.job).data


class InputReferredJobParamsSerializer(serializers.Serializer):
    technician_id: serializers.UUIDField(required=False, default=None)
    referred_by_id: serializers.UUIDField(required=False, default=None)
    updated_by_id = serializers.UUIDField(required=False, default=None),
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


class InputPublicReferredJobParamsSerializer(serializers.Serializer):
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