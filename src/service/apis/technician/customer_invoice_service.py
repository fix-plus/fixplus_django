from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from src.common.mixins import IsTechnicianMixin
from src.service.serializers.technician.customer_invoice_service import InputCustomerInvoiceServiceSerializer
from src.service.services.technician.customer_invoice_service import customer_invoice_service


class CustomerInvoiceServiceApi(IsTechnicianMixin, APIView):
    @extend_schema(
        summary="Update Customer Invoice Service",
        request=InputCustomerInvoiceServiceSerializer,
    )
    def patch(self, request, service_id):
        serializer = InputCustomerInvoiceServiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Core
        customer_invoice_service(
            service_id=service_id,
            technician=request.user,
            **serializer.validated_data,
        )

        # Response
        return Response({"result": _("Service status was updated.")}, status=status.HTTP_200_OK)