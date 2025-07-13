from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.views import APIView

from src.common.mixins import IsSuperAdminMixin
from src.common.pagination import LimitOffsetPagination, get_paginated_response_context
from src.parametric.selectors.device import search_device_type_list
from src.parametric.serializers.device import InputDeviceTypeParametricSerializer, OutPutDeviceTypeParametricSerializer
from src.parametric.services.device_type import create_device_type


class CreateDeviceTypeParametricApi(IsSuperAdminMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 100

    @extend_schema(
        summary="Create Device Type",
        request=InputDeviceTypeParametricSerializer,
        responses=OutPutDeviceTypeParametricSerializer,
    )
    def post(self, request):
        # user_groups = request.user.groups.values_list('name', flat=True)
        # if 'SUPER_ADMIN' not in user_groups:
        #     raise CustomAPIException(message='You are not allowed to use this method.', status_code=status.HTTP_403_FORBIDDEN)

        serializer = InputDeviceTypeParametricSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_device_type(**serializer.validated_data)

        query_set = search_device_type_list()

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutPutDeviceTypeParametricSerializer,
            queryset=query_set,
            request=request,
            view=self,
        )


class DeviceTypeParametricDetailApi(IsSuperAdminMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = search_device_type_list()
    serializer_class = OutPutDeviceTypeParametricSerializer