from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from src.common.mixins import IsSuperAdminOrAdminMixin
from src.common.pagination import get_paginated_response_context, LimitOffsetPagination
from src.customer.selectors.customer import search_customer_list, get_customer
from src.customer.serializers.customer import InputCustomerParamsSerializer, OutPutCustomerSerializer, \
    InputCustomerSerializer
from src.customer.services.customer import create_customer, update_customer, delete_customer


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

        db_customer_list = search_customer_list(
            **query_serializer.validated_data
        )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutPutCustomerSerializer,
            queryset=db_customer_list,
            request=request,
            view=self,
        )

    @extend_schema(
        summary="Create New Customer",
        request=InputCustomerSerializer,
        responses=OutPutCustomerSerializer)
    def post(self, request):
        serializer = InputCustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_customer(
            created_by=request.user,
            **serializer.validated_data
        )

        queryset = search_customer_list()

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutPutCustomerSerializer,
            queryset=queryset,
            request=request,
            view=self,
        )


class CustomerDetailApi(IsSuperAdminOrAdminMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        summary="Update Customer",
        request=InputCustomerSerializer,
        responses=OutPutCustomerSerializer)
    def patch(self, request, customer_id):
        serializer = InputCustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = get_customer(id=customer_id)

        update_customer(
            updated_by=request.user,
            instance=instance,
            **serializer.validated_data
        )

        queryset = search_customer_list()

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutPutCustomerSerializer,
            queryset=queryset,
            request=request,
            view=self,
        )

    @extend_schema(
        summary="Delete Customer",
        responses=OutPutCustomerSerializer)
    def delete(self, request, customer_id):
        instance = get_customer(id=customer_id)

        delete_customer(
            instance=instance,
        )

        queryset = search_customer_list()

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutPutCustomerSerializer,
            queryset=queryset,
            request=request,
            view=self,
        )