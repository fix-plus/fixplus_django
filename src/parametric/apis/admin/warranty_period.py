from rest_framework import generics
from rest_framework.views import APIView

from src.common.mixins import IsSuperAdminMixin
from src.common.pagination import LimitOffsetPagination, get_paginated_response_context
from src.parametric.selectors.warranty_period import search_warranty_period_list
from src.parametric.serializers.warranty_period import InputWarrantyPeriodParametricSerializer, OutPutWarrantyPeriodParametricSerializer
from src.parametric.services.warranty_period import create_warranty_period


class CreateWarrantyPeriodParametricApi(IsSuperAdminMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 100

    def post(self, request):
        # user_groups = request.user.groups.values_list('name', flat=True)
        # if 'SUPER_ADMIN' not in user_groups:
        #     raise CustomAPIException(message=_('You are not allowed to use this method.'), status_code=status.HTTP_403_FORBIDDEN)

        serializer = InputWarrantyPeriodParametricSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_warranty_period(**serializer.validated_data)

        query_set = search_warranty_period_list()
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutPutWarrantyPeriodParametricSerializer,
            queryset=query_set,
            request=request,
            view=self,
        )


class WarrantyPeriodParametricDetailApi(IsSuperAdminMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = search_warranty_period_list()
    serializer_class = OutPutWarrantyPeriodParametricSerializer