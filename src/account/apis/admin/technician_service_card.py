from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from src.common.mixins import IsSuperAdminOrAdminMixin
from src.common.pagination import LimitOffsetPagination, get_paginated_response_context
from src.account.selectors.technician_service_card import search_technician_service_card, get_technician_service_card
from src.account.serializers.admin.technician_service_card import InputTechnicianServiceCardParamsSerializer, OutputTechnicianServiceCardSerializer, \
    InputTechnicianServiceCardSerializer, InputUpdateTechnicianServiceCardSerializer
from src.account.services.technician_service_card import create_technician_service_card, update_technician_service_card, delete_technician_service_card


class TechnicianServiceCardListApi(IsSuperAdminOrAdminMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        summary="Search Technician Service Card",
        parameters=[InputTechnicianServiceCardParamsSerializer],
        responses=OutputTechnicianServiceCardSerializer)
    def get(self, request, technician_id):
        query_serializer = InputTechnicianServiceCardParamsSerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        db_technician_service_card_list = search_technician_service_card(
            **query_serializer.validated_data,
            technician_id=technician_id,
        )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutputTechnicianServiceCardSerializer,
            queryset=db_technician_service_card_list,
            request=request,
            view=self,
        )

    @extend_schema(
        summary="Create Technician Service Card",
        request=InputTechnicianServiceCardSerializer,
        responses=OutputTechnicianServiceCardSerializer
    )
    def post(self, request, technician_id):
        serializer = InputTechnicianServiceCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_technician_service_card(
            **serializer.validated_data,
            technician_id=technician_id,
        )

        db_technician_service_card_list = search_technician_service_card(
            technician_id=technician_id
        )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutputTechnicianServiceCardSerializer,
            queryset=db_technician_service_card_list,
            request=request,
            view=self,
        )


class TechnicianServiceCardDetailApi(IsSuperAdminOrAdminMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        summary="Update Technician Service Card",
        request=InputUpdateTechnicianServiceCardSerializer,
        responses=OutputTechnicianServiceCardSerializer
    )
    def patch(self, request, service_card_id):
        serializer = InputUpdateTechnicianServiceCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        db_technician_service_card = get_technician_service_card(id=service_card_id)
        update_technician_service_card(
            instance=db_technician_service_card,
            **serializer.validated_data
        )

        db_technician_service_card_list = search_technician_service_card(
            technician_id=db_technician_service_card.user.id
        )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutputTechnicianServiceCardSerializer,
            queryset=db_technician_service_card_list,
            request=request,
            view=self,
        )

    @extend_schema(
        summary="Delete Technician Service Card",
        responses=OutputTechnicianServiceCardSerializer
    )
    def delete(self, request, service_card_id):
        db_technician_service_card = get_technician_service_card(id=service_card_id)
        delete_technician_service_card(
            instance=db_technician_service_card,
        )

        db_technician_service_card_list = search_technician_service_card(
            technician_id=db_technician_service_card.user.id
        )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutputTechnicianServiceCardSerializer,
            queryset=db_technician_service_card_list,
            request=request,
            view=self,
        )