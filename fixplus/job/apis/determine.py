from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from fixplus.common.mixins import IsTechnicianMixin
from fixplus.job.serializers.determine import InputDetermineReferredJobWithTechnicianSerializer
from fixplus.job.serializers.job import InputJobSerializer
from fixplus.job.services.determine import update_determine_referred_job_with_technician


class DetermineReferredJobWithTechnicianApi(IsTechnicianMixin, APIView):
    @extend_schema(
        summary="Determine Referred Job With Technician",
        request=InputJobSerializer,
    )
    def patch(self, request):
        serializer = InputDetermineReferredJobWithTechnicianSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            determine_referred_job = update_determine_referred_job_with_technician(
                technician=request.user,
                **serializer.validated_data
            )

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"result": _("The status of the referred job was successfully determined.")}, status=status.HTTP_201_CREATED)