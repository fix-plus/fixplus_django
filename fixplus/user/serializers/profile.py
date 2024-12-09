from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from fixplus.upload.serializers import IdentifyDocumentMediaSerializer
from fixplus.upload.validators import FileSizeValidator, ImageSizeValidator
from fixplus.user.models import Profile
from fixplus.user.selectors.profile import get_land_line_numbers, get_mobile_numbers


class OutPutNumbersSerializer(serializers.Serializer):
    number = serializers.CharField()


class OutPutProfileSerializer(serializers.ModelSerializer):
    mobile = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    land_line_numbers = serializers.SerializerMethodField()
    mobile_numbers = serializers.SerializerMethodField()
    identify_document_photo = IdentifyDocumentMediaSerializer()
    other_identify_document_photos = IdentifyDocumentMediaSerializer(many=True)
    status = serializers.SerializerMethodField()
    is_verified_mobile = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = "__all__"

    def get_mobile(self, obj):
        return obj.user.mobile if obj.user else None

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.avatar:
            return request.build_absolute_uri(obj.avatar.url) if request else obj.avatar.url
        return None

    def get_land_line_numbers(self, obj):
        return [number['number'] for number in OutPutNumbersSerializer(get_land_line_numbers(obj.user), many=True).data]

    def get_mobile_numbers(self, obj):
        return [number['number'] for number in OutPutNumbersSerializer(get_mobile_numbers(obj.user), many=True).data]

    def get_status(self, obj):
        return obj.user.status if obj.user else None

    def get_is_verified_mobile(self, obj):
        return obj.user.is_verified_mobile if obj.user else None

    def get_groups(self, obj):
        groups = list(obj.user.groups.values_list('name', flat=True))
        return groups

    def get_permissions(self, obj):
        permissions = list(obj.user.user_permissions.values_list('codename', flat=True))
        return permissions


class InputUpdateProfileSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=False, allow_null=True, default=None, max_length=200)
    national_code = serializers.IntegerField(required=False, allow_null=True, default=None)
    gender = serializers.ChoiceField(required=False, allow_null=True, default=None, choices=['female', 'male'])
    address = serializers.CharField(required=False, allow_null=True, default=None)
    latitude = serializers.FloatField(required=False, allow_null=True, default=None)
    longitude = serializers.FloatField(required=False, allow_null=True, default=None)
    description = serializers.CharField(required=False, allow_null=True, default=None)
    avatar = serializers.ImageField(required=False, allow_null=True, default=None, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
        FileSizeValidator(min_size=1, max_size=10 * 1024 * 1024),
        ImageSizeValidator(max_height=4000, min_height=1, max_width=3000, min_width=1)
    ])
    land_line_numbers = serializers.ListField(required=False, child=serializers.CharField(), default=None)
    mobile_numbers = serializers.ListField(required=False, child=serializers.CharField(), default=None)
    identify_document_photo_id = serializers.UUIDField(required=False, default=None)
    other_identify_document_photos_id = serializers.ListField(required=False, default=None, child=serializers.CharField())


