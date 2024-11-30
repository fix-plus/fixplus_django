import re

from django.contrib.auth import authenticate
from django.core.validators import MinLengthValidator, MaxLengthValidator
from rest_framework import serializers
from rest_framework import status


from fixplus.user.models import BaseUser
from fixplus.user.selectors.user import is_exist_user, get_cache_verification_mobile_otp


class InputSignInUpSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=255, required=True)

    def validate_mobile(self, mobile):
        if mobile is None:
            return None

        # Regular expression to validate and format the mobile number
        pattern = r'^(00|\+)\d+$'

        if not re.match(pattern, mobile):
            raise serializers.ValidationError({"detail": "Mobile number must start with '00' or '+' and contain only digits after that."})

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
                {"detail": "Mobile number must start with '00' or '+' and contain only digits after that."})

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
            raise serializers.ValidationError({"detail": "Mobile number must start with '00' or '+' and contain only digits after that."})

        # Replace '00' with '+'
        if mobile.startswith('00'):
            mobile = '+' + mobile[2:]

        return mobile


class OutputTokensUserSerializer(serializers.Serializer):
    class TokenSerializers(serializers.Serializer):
        access = serializers.CharField()
        refresh = serializers.CharField()

    tokens = TokenSerializers()
    is_verified_mobile = serializers.BooleanField()
    is_admin = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    is_technician = serializers.BooleanField()
    status = serializers.CharField()