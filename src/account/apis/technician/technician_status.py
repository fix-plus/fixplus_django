from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.account.serializers.technician.technician_status import OutputTechnicianStatusSerializer, InputTechnicianStatusSerializer
from src.account.services.technician_status import create_technician_status
from src.common.mixins import IsVerifiedMobileMixin


class TechnicianStatusApi(IsVerifiedMobileMixin, APIView):
    @extend_schema(
        summary="Update Technician Status",
        request=InputTechnicianStatusSerializer,
        responses=OutputTechnicianStatusSerializer)
    def patch(self, request):
        serializer = InputTechnicianStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        db_user_profile = create_technician_status(
            user=request.user,
            **serializer.validated_data
        )

        return Response(OutputTechnicianStatusSerializer(db_user_profile, context={"request": request}).data, status=status.HTTP_201_CREATED)