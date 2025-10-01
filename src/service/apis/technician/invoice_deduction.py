from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from src.common.mixins import IsTechnicianMixin
from src.service.selectors.service import get_service

from src.service.serializers.technician.invoice_deduction import InputInvoiceDeductionSerializer
from src.service.services.technician.invoice_deduction import create_invoice_deduction


class TechnicianInvoiceDeductionApi(IsTechnicianMixin, APIView):
    @extend_schema(
        summary="Create Invoice Deduction",
        request=InputInvoiceDeductionSerializer,
    )
    def post(self, request, service_id):
        serializer = InputInvoiceDeductionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # initiate
        technician = request.user
        service = get_service(id=service_id)

        # Core
        create_invoice_deduction(
            technician=technician,
            service=service,
            **serializer.validated_data,
        )

        # Response
        return Response({"result": _("Service status was updated.")}, status=status.HTTP_200_OK)