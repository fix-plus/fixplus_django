from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class InputCustomerServiceSignatureSerializer(serializers.Serializer):
    image_id = serializers.UUIDField(required=True)

