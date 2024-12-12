from django.urls import reverse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from fixplus.common.mixins import IsVerifiedMobileMixin
from fixplus.upload.serializers import InputParamsUploadSerializer, InputUploadSerializer, OutPutUploadSerializer
from fixplus.upload.services import create_upload_identify_document_media


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

        try:
            if method.validated_data.get('method') == 'identify_document':
                created_db_upload = create_upload_identify_document_media(
                    user=request.user,
                    id=serializer.validated_data.get("id"),
                    image=serializer.validated_data.get("image")
                )

            else:
                raise Exception("This method not supported.")

        except Exception as ex:
            return Response(
                {'error': str(ex)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(OutPutUploadSerializer(created_db_upload, context={"request": request}).data)
