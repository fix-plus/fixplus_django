from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from src.common.mixins import IsSuperAdminOrAdminMixin
from src.common.pagination import get_paginated_response_context, LimitOffsetPagination
from src.service.selectors.technician_for_service import search_technician_for_service
from src.service.serializers.technician_for_service import InputTechnicianForServiceParamsSerializer, \
    OutPutTechnicianForServiceSerializer


class TechnicianForServiceListApi(IsSuperAdminOrAdminMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        summary="Search Technician for Job List",
        parameters=[InputTechnicianForServiceParamsSerializer],
        responses=OutPutTechnicianForServiceSerializer,
    )
    def get(self, request, uuid):
        query_serializer = InputTechnicianForServiceParamsSerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        # Queryset
        queryset = search_technician_for_service(
            service_id = uuid,
            **query_serializer.validated_data
        )

        # Response
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutPutTechnicianForServiceSerializer,
            queryset=queryset,
            request=request,
            view=self,
        )