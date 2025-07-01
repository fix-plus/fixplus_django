from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from src.common.mixins import IsSuperAdminOrAdminMixin
from src.common.pagination import LimitOffsetPagination, get_paginated_response_context
from src.account.selectors.technician_service_zone import search_technician_service_zone, get_technician_service_zone
from src.account.serializers.technician_service_zone import InputTechnicianServiceZoneParamsSerializer, OutputTechnicianServiceZoneSerializer, \
    InputTechnicianServiceZoneSerializer, InputUpdateTechnicianServiceZoneSerializer
from src.account.services.technician_service_zone import create_technician_service_zone, update_technician_service_zone, delete_technician_service_zone


class TechnicianServiceZoneListApi(IsSuperAdminOrAdminMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        summary="Search Technician Service Zone",
        parameters=[InputTechnicianServiceZoneParamsSerializer],
        responses=OutputTechnicianServiceZoneSerializer)
    def get(self, request, uuid):
        query_serializer = InputTechnicianServiceZoneParamsSerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        db_technician_service_zone_list = search_technician_service_zone(
            **query_serializer.validated_data,
            technician_id=uuid,
        )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutputTechnicianServiceZoneSerializer,
            queryset=db_technician_service_zone_list,
            request=request,
            view=self,
        )

    @extend_schema(
        summary="Create Technician Service Zone",
        request=InputTechnicianServiceZoneSerializer,
        responses=OutputTechnicianServiceZoneSerializer
    )
    def post(self, request, uuid):
        serializer = InputTechnicianServiceZoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_technician_service_zone(
            **serializer.validated_data,
            technician_id=uuid,
        )

        db_technician_service_zone_list = search_technician_service_zone(
            technician_id=uuid
        )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutputTechnicianServiceZoneSerializer,
            queryset=db_technician_service_zone_list,
            request=request,
            view=self,
        )


class TechnicianServiceZoneDetailApi(IsSuperAdminOrAdminMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        summary="Update Technician Service Zone",
        request=InputUpdateTechnicianServiceZoneSerializer,
        responses=OutputTechnicianServiceZoneSerializer
    )
    def patch(self, request, service_zone_id):
        serializer = InputUpdateTechnicianServiceZoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        db_technician_service_zone_list = get_technician_service_zone(id=service_zone_id)
        update_technician_service_zone(
            instance=db_technician_service_zone_list,
            **serializer.validated_data
        )

        db_technician_service_zone_list = search_technician_service_zone(
            technician_id=db_technician_service_zone_list.user.id
        )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutputTechnicianServiceZoneSerializer,
            queryset=db_technician_service_zone_list,
            request=request,
            view=self,
        )

    @extend_schema(
        summary="Delete Technician Service Zone",
        responses=OutputTechnicianServiceZoneSerializer
    )
    def delete(self, request, service_zone_id):
        db_technician_service_zone_list = get_technician_service_zone(id=service_zone_id)
        delete_technician_service_zone(
            instance=db_technician_service_zone_list,
        )

        db_technician_service_zone_list = search_technician_service_zone(
            technician_id=db_technician_service_zone_list.user.id
        )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutputTechnicianServiceZoneSerializer,
            queryset=db_technician_service_zone_list,
            request=request,
            view=self,
        )