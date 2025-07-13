from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from src.common.mixins import IsRegisteredMixin
from src.common.pagination import LimitOffsetPagination, get_paginated_response_context
from src.parametric.selectors.device import search_device_type_list
from src.parametric.serializers.device import OutPutDeviceTypeParametricSerializer


class GetDeviceTypeParametricApi(IsRegisteredMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 100

    @extend_schema(
        summary="Get Device Type List",
        responses=OutPutDeviceTypeParametricSerializer,
    )
    def get(self, request):
        query_set = search_device_type_list()

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutPutDeviceTypeParametricSerializer,
            queryset=query_set,
            request=request,
            view=self,
        )

