# users/serializers/users.py
import re

from rest_framework import serializers
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from fixplus.user.models import BaseUser
from fixplus.user.serializers.profile import OutPutProfileSerializer


class InputUserParamsSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=False, default=None)
    status = serializers.CharField(required=False, default=None)
    full_name = serializers.CharField(required=False, default=None)
    group = serializers.CharField(required=False, default=None)
    sort_by = serializers.ChoiceField(required=False, default=None, choices=['created_at', 'last_online', 'request_register_datetime'])
    order = serializers.CharField(required=False, default=None)

    def validate_mobile(self, mobile):
        if mobile is None:
            return None

        # Regular expression to validate and format the mobile number
        pattern = r'^(00|\+)\d+$'

        if not re.match(pattern, mobile):
            raise serializers.ValidationError({"detail": _("Mobile number must start with '00' or '+' and contain only digits after that.")})

        # Replace '00' with '+'
        if mobile.startswith('00'):
            mobile = '+' + mobile[2:]

        return mobile


class InputUserSerializer(serializers.Serializer):
    status = serializers.ChoiceField(required=False, default=None, choices=['not_registered', 'checking', 'registered', 'rejected'])
    reason_for_rejected = serializers.CharField(required=False, default=None)


class OutPutUserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)

    class Meta:
        model = BaseUser
        fields = ['mobile', 'id', 'groups', 'status', 'is_active', 'is_verified_mobile', 'last_login', 'last_online', 'created_at', 'updated_at', 'request_register_datetime', 'reason_for_rejected']


class OutPutUserDetailSerializer(serializers.ModelSerializer):
    profile = OutPutProfileSerializer()

    class Meta:
        model = BaseUser
        fields = ['mobile', 'id', 'status', 'is_active', 'is_verified_mobile', 'profile', 'last_login', 'last_online', 'created_at', 'updated_at', 'request_register_datetime']
