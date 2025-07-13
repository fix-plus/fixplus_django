from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from src.common.mixins import IsTechnicianMixin
from src.common.pagination import LimitOffsetPagination, get_paginated_response_context
from src.service.selectors.service import search_service_list
from src.service.serializers.shared.service import OutPutServiceSerializer, InputServiceParamsSerializer


class TechnicianServiceListApi(IsTechnicianMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        summary="Search Service List",
        parameters=[InputServiceParamsSerializer],
        responses=OutPutServiceSerializer)
    def get(self, request):
        query_serializer = InputServiceParamsSerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        user = request.user

        # Queryset
        queryset = search_service_list(
            technician_id=user.id,
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