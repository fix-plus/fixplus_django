from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class InputAcceptServiceSerializer(serializers.Serializer):
    is_accepted = serializers.BooleanField(required=True)
    estimate_arrival_at = serializers.DateTimeField(required=False, default=None)
    reject_reason = serializers.CharField(required=False, default=None, allow_blank=True)

    def validate(self, attrs):
        # Check if is_accepted is True and estimate_arrival_at is provided
        if attrs.get('is_accepted') and not attrs.get('estimate_arrival_at'):
            raise serializers.ValidationError({"estimate_arrival_at": _("This field is required when accepting the service.")})

        # Check if is_accepted is False and reject_reason is provided
        if not attrs.get('is_accepted') and not attrs.get('reject_reason'):
            raise serializers.ValidationError({"reject_reason": _("This field is required when rejecting the service.")})

        return attrs

