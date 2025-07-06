from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from src.common.mixins import IsSuperAdminOrAdminMixin
from src.common.pagination import LimitOffsetPagination, get_paginated_response_context
from src.service.selectors.service import search_service_list
from src.service.serializers.service import InputServiceSerializer, OutPutServiceSerializer, InputServiceParamsSerializer
from src.service.services.service import create_service


class ServiceListApi(IsSuperAdminOrAdminMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        summary="Search Service List",
        parameters=[InputServiceParamsSerializer],
        responses=OutPutServiceSerializer)
    def get(self, request):
        query_serializer = InputServiceParamsSerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        # Queryset
        queryset = search_service_list(
            **query_serializer.validated_data
        )

        # Response
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutPutServiceSerializer,
            queryset=queryset,
            request=request,
            view=self,
        )

    @extend_schema(
        summary="Create New Service",
        request=InputServiceSerializer,
        responses=OutPutServiceSerializer
    )
    def post(self, request):
        serializer = InputServiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Core
        create_service(
            created_by=request.user,
            **serializer.validated_data
        )

        # Response
        return Response({"result": _("Successfully placed in the assign queue.")}, status=status.HTTP_201_CREATED)