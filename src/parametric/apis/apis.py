from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from src.common.custom_exception import CustomAPIException
from src.common.mixins import IsSuperAdminMixin, IsRegisteredMixin
from src.common.pagination import LimitOffsetPagination, get_paginated_response_context
from src.parametric.selectors.selectors import search_brand_name_list, get_timing_setting, search_device_type_list
from src.parametric.serializers.serializers import (
    OutPutBrandNameParametricSerializer,
    InputBrandNameParametricSerializer,
    OutPutDeviceTypeParametricSerializer,
    OutPutTimingSettingParametricSerializer,
    InputTimingSettingParametricSerializer,
    InputDeviceTypeParametricSerializer
)


class BrandNameParametricApi(IsRegisteredMixin, APIView):
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

    @extend_schema(
        summary="Create Brand Name",
        request=InputBrandNameParametricSerializer,
    )
    def post(self, request):
        user_groups = request.user.groups.values_list('name', flat=True)

        if 'super_admin' not in user_groups:
            raise CustomAPIException(message=_('You are not allowed to use this method.'), status_code=status.HTTP_403_FORBIDDEN)

        serializer = InputBrandNameParametricSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

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


class DeviceTypeParametricApi(IsRegisteredMixin, APIView):
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

    @extend_schema(
        summary="Create Device Type",
        request=InputDeviceTypeParametricSerializer,
    )
    def post(self, request):
        user_groups = request.user.groups.values_list('name', flat=True)

        if 'super_admin' not in user_groups:
            raise CustomAPIException(message='You are not allowed to use this method.', status_code=status.HTTP_403_FORBIDDEN)

        serializer = InputDeviceTypeParametricSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        query_set = search_device_type_list()

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutPutDeviceTypeParametricSerializer,
            queryset=query_set,
            request=request,
            view=self,
        )


class DeviceTypeParametricDetailApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = search_device_type_list()
    serializer_class = OutPutDeviceTypeParametricSerializer


class TimingSettingParametricApi(IsRegisteredMixin, APIView):
    @extend_schema(
        summary="Get Timing Setting List",
        responses=OutPutTimingSettingParametricSerializer,
    )
    def get(self, request):
        query_set = get_timing_setting()

        return Response(OutPutTimingSettingParametricSerializer(query_set).data)

    @extend_schema(
        summary="Update Timing Setting",
        request=InputTimingSettingParametricSerializer,
    )
    def patch(self, request):
        user_groups = request.user.groups.values_list('name', flat=True)

        if 'super_admin' not in user_groups:
            raise CustomAPIException(message=_('You are not allowed to use this method.'), status_code=status.HTTP_403_FORBIDDEN)

        instance = get_timing_setting()

        if not instance:
            raise CustomAPIException(message=_('Timing setting not found.'), status_code=status.HTTP_404_NOT_FOUND)

        serializer = InputTimingSettingParametricSerializer(instance, data=request.data, partial=True)  # Use partial=True for PATCH
        serializer.is_valid(raise_exception=True)

        serializer.save()  # Save the updated instance
        updated_instance = get_timing_setting()  # Fetch the updated instance

        return Response(OutPutTimingSettingParametricSerializer(updated_instance).data)