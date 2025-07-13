from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from src.common.mixins import IsRegisteredMixin
from src.common.pagination import LimitOffsetPagination, get_paginated_response_context
from src.parametric.selectors.brand import search_brand_name_list
from src.parametric.serializers.brand import OutPutBrandNameParametricSerializer


class GetBrandNameParametricApi(IsRegisteredMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 100

    @extend_schema(
        summary="Get Brand Name List",
        responses=OutPutBrandNameParametricSerializer,
    )
    def get(self, request):
        query_set = search_brand_name_list()

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutPutBrandNameParametricSerializer,
            queryset=query_set,
            request=request,
            view=self,
        )