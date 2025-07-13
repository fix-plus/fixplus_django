from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from src.common.mixins import IsTechnicianMixin

from src.service.serializers.technician.accept_service import InputAcceptServiceSerializer
from src.service.services.technician.accept_service import accept_service


class TechnicianAcceptServiceApi(IsTechnicianMixin, APIView):
    @extend_schema(
        summary="Update Technician Accept Service",
        request=InputAcceptServiceSerializer,
    )
    def patch(self, request, service_id):
        serializer = InputAcceptServiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Core
        accept_service(
            service_id=service_id,
            user=request.user,
            **serializer.validated_data,
        )

        # Response
        return Response({"result": _("Service status was updated.")}, status=status.HTTP_200_OK)