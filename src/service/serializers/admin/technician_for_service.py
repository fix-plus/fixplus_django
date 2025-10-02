import re

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from src.account.serializers.shared.contact_number import OutPutContactNumberSerializer
from src.account.serializers.admin.technician_service_zone import OutputTechnicianServiceZoneSerializer
from src.authentication.models.user import User
from src.account.models import Profile
from src.communication.selectors.admin_pin_message_of_technician import get_latest_admin_pin_message_of_technician
from src.communication.serializers.admin_pin_message_of_technician import OutputAdminPinMessageOfTechnicianSerializer
from src.geo.serializers.address import OutPutAddressSerializer
from src.geo.serializers.user_location_tracker import OutputUserLocationTrackerSerializer


class InputTechnicianForServiceParamsSerializer(serializers.Serializer):
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


class OutPutTechnicianForServiceSerializer(serializers.ModelSerializer):
    class OutPutProfileSerializer(serializers.ModelSerializer):
        mobile = serializers.SerializerMethodField()
        avatar = serializers.SerializerMethodField()
        contact_numbers = serializers.SerializerMethodField()
        address = OutPutAddressSerializer()

        class Meta:
            model = Profile
            fields = ['full_name', 'mobile', 'avatar', 'contact_numbers', 'address',]

        def get_mobile(self, obj):
            return obj.user.mobile if obj.user else None

        def get_avatar(self, obj):
            request = self.context.get('request')
            if obj.avatar:
                return request.build_absolute_uri(obj.avatar.url) if request else obj.avatar.url
            return None

        def get_contact_numbers(self, obj):
            return OutPutContactNumberSerializer(obj.user.contact_numbers, many=True).data


    profile = serializers.SerializerMethodField()
    distance = serializers.FloatField(default=None)
    latest_location = serializers.SerializerMethodField()
    in_processing_count = serializers.SerializerMethodField()
    rejected_count = serializers.SerializerMethodField()
    done_count = serializers.SerializerMethodField()
    pin_message_of_technician = serializers.SerializerMethodField()
    service_zone = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['mobile', 'id', 'profile', 'distance', 'last_online', 'latest_location', 'in_processing_count', 'rejected_count', 'done_count', 'pin_message_of_technician', 'service_zone']

    def get_profile(self, obj):
        return self.OutPutProfileSerializer(obj.profile, context=self.context).data

    def get_latest_location(self, obj):
        try:
            queryset = obj.location_trackers.latest('created_at')
        except obj.location_trackers.model.DoesNotExist:
            return None
        return OutputUserLocationTrackerSerializer(queryset).data



    def get_in_processing_count(self, obj):
        return 3
    #
    def get_rejected_count(self, obj):
        return 12

    def get_done_count(self, obj):
        return 4

    def get_pin_message_of_technician(self, obj):
        queryset = get_latest_admin_pin_message_of_technician(user=obj)
        return OutputAdminPinMessageOfTechnicianSerializer(queryset).data if queryset else None

    def get_service_zone(self, obj):
        queryset = obj.technician_service_zone
        return OutputTechnicianServiceZoneSerializer(queryset, many=True).data if queryset else None