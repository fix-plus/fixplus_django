from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from src.common.mixins import IsTechnicianMixin
from src.media.selectors import get_upload_customer_signature_media
from src.service.selectors.service import get_service
from src.service.serializers.technician.customer_service_signature import InputCustomerServiceSignatureSerializer

from src.service.services.technician.customer_service_signature import create_customer_service_signature


class CustomerServiceSignatureApi(IsTechnicianMixin, APIView):
    @extend_schema(
        summary="Create Customer Service Signature",
        request=InputCustomerServiceSignatureSerializer,
    )
    def post(self, request, service_id):
        serializer = InputCustomerServiceSignatureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Initialize
        service = get_service(id=service_id)
        image = get_upload_customer_signature_media(serializer.validated_data.get("image_id"))

        # Core
        create_customer_service_signature(
            service=service,
            image=image,
        )

        # Response
        return Response({"result": _("Customer Signature was updated.")}, status=status.HTTP_200_OK)