from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from src.common.mixins import IsTechnicianMixin
from src.payment.serializers.technician_online_payment import InputInitiateTechnicianOnlinePaymentSerializer
from src.payment.services.online_payment import initiate_technician_online_payment


class InitiateTechnicianOnlinePaymentApi(IsTechnicianMixin, APIView):
    @extend_schema(
        summary="Initiate Technician Online Payment",
    )
    def post(self, request):
        serializer = InputInitiateTechnicianOnlinePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        result = initiate_technician_online_payment(
            technician=user,
            request=request,
            **serializer.validated_data,
        )

        return Response(result, status=status.HTTP_200_OK)

