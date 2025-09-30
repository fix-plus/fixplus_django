from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from src.common.mixins import IsTechnicianMixin
from src.payment.serializers.customer_payment import InputCustomerPaymentSerializer, OutputCustomerPaymentSerializer, \
    InputVerifyCustomerPaymentSerializer
from src.payment.services.customer_payment import create_customer_payment, verify_customer_payment_with_online
from src.service.selectors.service import get_service


class CreateCustomerPaymentApi(IsTechnicianMixin, APIView):
    @extend_schema(
        summary="Create Customer Payment",
        request=InputCustomerPaymentSerializer,
        responses=OutputCustomerPaymentSerializer,
    )
    def post(self, request):
        serializer = InputCustomerPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        service = get_service(id=serializer.validated_data.get("service_id"))

        result = create_customer_payment(
            technician=user,
            request=request,
            service=service,
            **serializer.validated_data,
        )

        return Response(OutputCustomerPaymentSerializer(result).data, status=status.HTTP_200_OK)


class VerifyCustomerPaymentApi(IsTechnicianMixin, APIView):
    @extend_schema(
        summary="Verify Customer Payment",
        request=InputVerifyCustomerPaymentSerializer,
        responses=OutputCustomerPaymentSerializer,
    )
    def post(self, request):
        serializer = InputVerifyCustomerPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        service = get_service(id=serializer.validated_data.get("service_id"))

        result = verify_customer_payment_with_online(
            technician=user,
            service=service,
        )

        return Response(OutputCustomerPaymentSerializer(result).data, status=status.HTTP_200_OK)

