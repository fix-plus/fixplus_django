# users/serializers/users.py
import re

from rest_framework import serializers
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from src.authentication.models import User
from src.account.serializers.profile import OutPutProfileSerializer, InputUpdateProfileSerializer

class InputUserParamsSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=False, default=None)
    registry_status = serializers.CharField(required=False, default=None)
    technician_status = serializers.CharField(required=False, default=None)
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
    status = serializers.ChoiceField(required=False, default=None, allow_null=True, choices=['draft', 'checking', 'approved', 'rejected'])
    rejected_reason = serializers.CharField(required=False, default=None, allow_null=True)
    group = serializers.ListField(required=False, default=None, child=serializers.CharField())
    profile = InputUpdateProfileSerializer(required=False, allow_null=True, default=None)


class OutPutUserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.user_type = kwargs.pop('user_type', None)
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        return OutPutProfileSerializer(instance.profile, context=self.context, user_type=self.user_type).data


# class OutPutSuperAdminUserDetailSerializer(serializers.ModelSerializer):
#     profile = serializers.SerializerMethodField()
#
#     class Meta:
#         model = User
#         fields = ['mobile', 'id', 'status', 'is_active', 'is_verified_mobile', 'profile', 'last_login', 'last_online', 'created_at', 'updated_at', 'request_register_datetime']
#
#     def get_profile(self, obj):
#         return OutPutProfileSerializer(obj.profile, context=self.context, user_type='super_admin').data
#
#
# class OutPutAdminUserDetailSerializer(serializers.ModelSerializer):
#     profile = serializers.SerializerMethodField()
#
#     class Meta:
#         model = User
#         fields = ['id', 'mobile', 'profile', 'last_login', 'last_online', 'created_at', ]
#
#     def get_profile(self, obj):
#         return OutPutProfileSerializer(obj.profile, context=self.context, user_type='admin').data
#
#
# class OutPutPublicUserDetailSerializer(serializers.ModelSerializer):
#     profile = serializers.SerializerMethodField()
#
#     class Meta:
#         model = User
#         fields = ['id', 'profile', 'last_online',]
#
#     def get_profile(self, obj):
#         return OutPutProfileSerializer(obj.profile, context=self.context, user_type='public').data
