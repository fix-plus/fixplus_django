from rest_framework import serializers

from fixplus.job.models import ReferredJob


class InputDetermineReferredJobWithTechnicianSerializer(serializers.Serializer):
    referred_job_id = serializers.UUIDField(required=True)
    status = serializers.ChoiceField(required=True, choices=['in_processing', 'rejected_by_technician'])
    estimated_arrival_at = serializers.DateTimeField(allow_null=True, required=False, default=None)
    rejected_reason_by_technician = serializers.CharField(allow_null=True, required=False, default=None)