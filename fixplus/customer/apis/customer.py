from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from fixplus.common.mixins import IsSuperAdminOrAdminMixin
from fixplus.common.pagination import get_paginated_response_context, LimitOffsetPagination
from fixplus.customer.selectors.selectors import search_customer_list
from fixplus.customer.serializers.serializers import InputCustomerParamsSerializer, OutPutCustomerSerializer


class CustomerListApi(IsSuperAdminOrAdminMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        summary="Search Customer List",
        parameters=[InputCustomerParamsSerializer],
        responses=OutPutCustomerSerializer)
    def get(self, request):
        query_serializer = InputCustomerParamsSerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        try:
            db_customer_list = search_customer_list(
                **query_serializer.validated_data
            )

        except Exception as ex:
            return Response(
                {'error': str(ex)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutPutCustomerSerializer,
            queryset=db_customer_list,
            request=request,
            view=self,
        )