from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from src.common.mixins import IsRegisteredMixin
from src.common.pagination import LimitOffsetPagination, get_paginated_response_context
from src.parametric.selectors.warranty_period import search_warranty_period_list
from src.parametric.serializers.warranty_period import OutPutWarrantyPeriodParametricSerializer


class GetWarrantyPeriodParametricApi(IsRegisteredMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 100

    @extend_schema(
        summary="Get Warranty Period List",
        responses=OutPutWarrantyPeriodParametricSerializer,
    )
    def get(self, request):
        query_set = search_warranty_period_list()

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutPutWarrantyPeriodParametricSerializer,
            queryset=query_set,
            request=request,
            view=self,
        )