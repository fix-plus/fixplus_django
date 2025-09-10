from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from src.account.selectors.technician_status import get_latest_technician_status
from src.account.serializers.shared.contact_number import OutPutContactNumberSerializer, InputContactNumbersSerializer
from src.geo.serializers.address import OutPutAddressSerializer
from src.geo.serializers.user_location_tracker import OutputUserLocationTrackerSerializer
from src.media.validators import FileSizeValidator, ImageSizeValidator
from src.account.models import Profile


class OutPutNumbersSerializer(serializers.Serializer):
    number = serializers.CharField()


class OutPutProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    last_online = serializers.SerializerMethodField()
    contact_numbers = serializers.SerializerMethodField()
    address = OutPutAddressSerializer()
    identify_document_photo = serializers.SerializerMethodField()
    other_identify_document_photos = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    technician_status = serializers.SerializerMethodField()
    latest_location = serializers.SerializerMethodField()
    rejected_reason = serializers.SerializerMethodField()
    is_verified_mobile = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    register_request_at = serializers.SerializerMethodField()


    class Meta:
        model = Profile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        user_type = kwargs.pop('user_type', None)
        super().__init__(*args, **kwargs)

        # BaseFields
        base_fields = ['user_id', 'full_name', 'gender', 'avatar', 'groups', 'technician_status', 'latest_location', 'last_online', 'created_at']

        if user_type == "super_admin" or user_type == "me":
            allowed_fields = base_fields + [
                "national_code", "mobile", "address","status", "rejected_reason", "is_verified_mobile",
                "description", "identify_document_photo", "other_identify_document_photos",
                "contact_numbers", "permissions", "register_request_at"
            ]
        elif user_type == "admin":
            allowed_fields = base_fields + [
                "mobile", "status", "contact_numbers", "address", "register_request_at"
            ]
        elif user_type == "admin_list":
            allowed_fields = base_fields + [
                "mobile", "address", "register_request_at"
            ]
        else:  # Public User
            allowed_fields = base_fields

        # Execute Final Fields
        for field_name in list(self.fields.keys()):
            if field_name not in allowed_fields:
                self.fields.pop(field_name)

    def get_user_id(self, obj):
        return obj.user.id

    def get_mobile(self, obj):
        return obj.user.mobile if obj.user else None

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.avatar:
            return request.build_absolute_uri(obj.avatar.url) if request else obj.avatar.url
        return None

    def get_last_online(self, obj):
        return obj.user.last_online if obj.user else None

    def get_contact_numbers(self, obj):
        return OutPutContactNumberSerializer(obj.user.contact_numbers, many=True).data

    def get_identify_document_photo(self, obj):
        request = self.context.get('request')
        if obj.user.registry_requests.exists():
            identify_doc = obj.user.registry_requests.latest('created_at').identify_document_photo
            if identify_doc:
                image_url = request.build_absolute_uri(identify_doc.image.url) if request else identify_doc.image.url
                return {
                    "id": str(identify_doc.id),
                    "image": image_url
                }
        return None

    def get_other_identify_document_photos(self, obj):
        request = self.context.get('request')
        if obj.user.registry_requests.exists():
            identify_docs = obj.user.registry_requests.latest('created_at').other_identify_document_photos.all()
            result = []
            for doc in identify_docs:
                if doc.image:
                    image_url = request.build_absolute_uri(doc.image.url) if request else doc.image.url
                    result.append({
                        "id": str(doc.id),
                        "image": image_url
                    })
            return result
        return []

    def get_status(self, obj):
        return obj.user.registry_requests.latest('created_at').status if obj.user.registry_requests.exists() else None

    def get_technician_status(self, obj):
        return get_latest_technician_status(user=obj.user).status if get_latest_technician_status(user=obj.user) else None

    def get_latest_location(self, obj):
        try:
            queryset = obj.user.location_trackers.latest('created_at')
        except obj.user.location_trackers.model.DoesNotExist:
            return None
        return OutputUserLocationTrackerSerializer(queryset).data

    def get_rejected_reason(self, obj):
        return obj.user.registry_requests.latest('created_at').rejected_reason if obj.user.registry_requests.exists() else None

    def get_is_verified_mobile(self, obj):
        return obj.user.is_verified_mobile if obj.user else None

    def get_groups(self, obj):
        groups = list(obj.user.groups.values_list('name', flat=True))
        return groups

    def get_permissions(self, obj):
        # Get account-specific permissions
        user_permissions = set(obj.user.user_permissions.values_list('codename', flat=True))

        # Get group permissions
        group_permissions = set()
        for group in obj.user.groups.all():
            group_permissions.update(group.permissions.values_list('codename', flat=True))

        # Combine both sets of permissions
        all_permissions = user_permissions.union(group_permissions)

        return list(all_permissions)

    def get_register_request_at(self, obj):
        if obj.user.registry_requests.exists():
            return obj.user.registry_requests.latest('created_at').created_at
        return None


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Remove technician_status field if user is not a technician
        if not instance.user.has_technician():
            representation.pop('technician_status', None)
            representation.pop('latest_location', None)
        return representation


class InputUpdateProfileSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=False, allow_null=True, default=None, max_length=200)
    national_code = serializers.CharField(required=False, allow_null=True, default=None)
    gender = serializers.ChoiceField(required=False, allow_null=True, default=None, choices=Profile.Gender.choices)
    address = serializers.CharField(required=False, allow_null=True, default=None)
    latitude = serializers.FloatField(required=False, allow_null=True, default=None)
    longitude = serializers.FloatField(required=False, allow_null=True, default=None)
    description = serializers.CharField(required=False, allow_null=True, default=None)
    is_in_holiday = serializers.BooleanField(required=False, allow_null=True, default=None)
    avatar = serializers.ImageField(required=False, allow_null=True, default=None, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
        FileSizeValidator(min_size=1, max_size=10 * 1024 * 1024),
        ImageSizeValidator(max_height=4000, min_height=1, max_width=3000, min_width=1)
    ])
    contact_numbers = serializers.ListField(required=False, child=InputContactNumbersSerializer(), default=None)
    identify_document_photo_id = serializers.UUIDField(required=False, default=None)
    other_identify_document_photos_id = serializers.ListField(required=False, default=None, child=serializers.CharField())


