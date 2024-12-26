import re

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from fixplus.job.selectors.referred import search_referred_job_list
from fixplus.user.models import BaseUser, Profile
from fixplus.user.selectors.profile import get_land_line_numbers, get_mobile_numbers
from fixplus.user.serializers.profile import OutPutNumbersSerializer


class InputTechnicianForJobParamsSerializer(serializers.Serializer):
    job_id = serializers.UUIDField(required=False, default=None, allow_null=True)
    mobile = serializers.CharField(required=False, default=None)
    full_name = serializers.CharField(required=False, default=None)
    sort_by = serializers.ChoiceField(required=False, default=None, choices=['created_at', 'last_online',])
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


class OutPutTechnicianForJobSerializer(serializers.ModelSerializer):
    class OutPutProfileSerializer(serializers.ModelSerializer):
        mobile = serializers.SerializerMethodField()
        avatar = serializers.SerializerMethodField()
        land_line_numbers = serializers.SerializerMethodField()
        mobile_numbers = serializers.SerializerMethodField()

        class Meta:
            model = Profile
            fields = ['full_name', 'mobile', 'avatar', 'land_line_numbers', 'mobile_numbers', 'address', 'latitude', 'longitude', 'is_in_holiday']

        def get_mobile(self, obj):
            return obj.user.mobile if obj.user else None

        def get_avatar(self, obj):
            request = self.context.get('request')
            if obj.avatar:
                return request.build_absolute_uri(obj.avatar.url) if request else obj.avatar.url
            return None

        def get_land_line_numbers(self, obj):
            return [number['number'] for number in
                    OutPutNumbersSerializer(get_land_line_numbers(obj.user), many=True).data]

        def get_mobile_numbers(self, obj):
            return [number['number'] for number in
                    OutPutNumbersSerializer(get_mobile_numbers(obj.user), many=True).data]


    profile = serializers.SerializerMethodField()
    in_processing_count = serializers.SerializerMethodField()
    rejected_count = serializers.SerializerMethodField()
    done_count = serializers.SerializerMethodField()

    class Meta:
        model = BaseUser
        fields = ['mobile', 'id', 'profile', 'last_online', 'in_processing_count', 'rejected_count', 'done_count', 'created_at', 'updated_at']

    def get_profile(self, obj):
        return self.OutPutProfileSerializer(obj.profile, context=self.context).data

    def get_in_processing_count(self, obj):
        return search_referred_job_list(technician_id=obj.id, status='in_processing').count()
    #
    def get_rejected_count(self, obj):
        return search_referred_job_list(technician_id=obj.id, status='rejected').count()

    def get_done_count(self, obj):
        return search_referred_job_list(technician_id=obj.id, status='done').count()