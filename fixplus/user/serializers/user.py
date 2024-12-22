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
    status = serializers.ChoiceField(required=False, default=None, allow_null=True, choices=['not_registered', 'checking', 'registered', 'rejected'])
    reason_for_rejected = serializers.CharField(required=False, default=None, allow_null=True)
    group = serializers.ListField(required=False, default=None, child=serializers.CharField())


class OutPutUserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)
    full_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = BaseUser
        fields = ['mobile', 'id', 'full_name', 'groups', 'status', 'is_active', 'is_verified_mobile', 'avatar', 'last_login', 'last_online', 'created_at', 'updated_at', 'request_register_datetime', 'reason_for_rejected']

    def get_full_name(self, obj):
        return obj.profile.full_name

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.profile.avatar:
            return request.build_absolute_uri(obj.profile.avatar.url) if request else obj.profile.avatar.url
        return None


class OutPutUserDetailSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = BaseUser
        fields = ['mobile', 'id', 'status', 'is_active', 'is_verified_mobile', 'profile', 'last_login', 'last_online', 'created_at', 'updated_at', 'request_register_datetime']

    def get_profile(self, obj):
        return OutPutProfileSerializer(obj.profile, context=self.context).data
