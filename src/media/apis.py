from django.urls import reverse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from src.common.custom_exception import CustomAPIException
from src.common.mixins import IsVerifiedMobileMixin
from src.media.serializers import InputParamsUploadSerializer, InputUploadSerializer, OutPutUploadSerializer
from src.media.services import create_upload_identify_document_media, create_upload_service_card_media, \
    create_upload_customer_signature_media


class UploadCenterApi(IsVerifiedMobileMixin, APIView):
    parser_classes = [MultiPartParser]
    
    @extend_schema(
        summary="Upload Center",
        parameters=[InputParamsUploadSerializer],
        request=InputUploadSerializer,
        responses=OutPutUploadSerializer)
    def post(self, request):
        method = InputParamsUploadSerializer(data=request.query_params)
        method.is_valid(raise_exception=True)
        serializer = InputUploadSerializer(data=request.data, context={"params": request.query_params})
        serializer.is_valid(raise_exception=True)

        if method.validated_data.get('method') == 'identify_document':
            created_db_upload = create_upload_identify_document_media(
                user=request.user,
                id=serializer.validated_data.get("id"),
                image=serializer.validated_data.get("image")
            )

        elif method.validated_data.get('method') == 'service_card':
            created_db_upload = create_upload_service_card_media(
                user=request.user,
                id=serializer.validated_data.get("id"),
                image=serializer.validated_data.get("image")
            )

        elif method.validated_data.get('method') == 'customer_signature':
            created_db_upload = create_upload_customer_signature_media(
                user=request.user,
                id=serializer.validated_data.get("id"),
                image=serializer.validated_data.get("image")
            )

        else:
            raise CustomAPIException("This method not supported.", status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

        return Response(OutPutUploadSerializer(created_db_upload, context={"request": request}).data)
