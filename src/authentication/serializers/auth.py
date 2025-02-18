import re

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class InputSignInUpSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=255, required=True)

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


class InputReSendVerificationCodeSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=255, required=True)

    def validate_mobile(self, mobile):
        if mobile is None:
            return None

        # Regular expression to validate and format the mobile number
        pattern = r'^(00|\+)\d+$'

        if not re.match(pattern, mobile):
            raise serializers.ValidationError(
                {"detail": _("Mobile number must start with '00' or '+' and contain only digits after that.")})

        # Replace '00' with '+'
        if mobile.startswith('00'):
            mobile = '+' + mobile[2:]

        return mobile


class InputConfirmVerificationCodeSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=255, required=True)
    code = serializers.CharField(min_length=4, max_length=4, required=True)

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


class OutPutTokensUserSerializer(serializers.Serializer):
    tokens = serializers.DictField()
    groups = serializers.ListField(child=serializers.CharField())
    permissions = serializers.ListField(child=serializers.CharField())
    is_verified_mobile = serializers.BooleanField()
    status = serializers.CharField()