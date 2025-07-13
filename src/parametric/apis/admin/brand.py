from rest_framework import generics
from rest_framework.views import APIView

from src.common.mixins import IsSuperAdminMixin
from src.common.pagination import LimitOffsetPagination, get_paginated_response_context
from src.parametric.selectors.brand import search_brand_name_list
from src.parametric.serializers.brand import InputBrandNameParametricSerializer, OutPutBrandNameParametricSerializer
from src.parametric.services.brand import create_brand


class CreateBrandNameParametricApi(IsSuperAdminMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 100

    def post(self, request):
        # user_groups = request.user.groups.values_list('name', flat=True)
        # if 'SUPER_ADMIN' not in user_groups:
        #     raise CustomAPIException(message=_('You are not allowed to use this method.'), status_code=status.HTTP_403_FORBIDDEN)

        serializer = InputBrandNameParametricSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_brand(**serializer.validated_data)

        query_set = search_brand_name_list()
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutPutBrandNameParametricSerializer,
            queryset=query_set,
            request=request,
            view=self,
        )


class BrandNameParametricDetailApi(IsSuperAdminMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = search_brand_name_list()
    serializer_class = OutPutBrandNameParametricSerializer