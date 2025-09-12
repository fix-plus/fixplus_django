from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from src.common.mixins import IsSuperAdminOrAdminMixin, IsTechnicianMixin
from src.common.pagination import LimitOffsetPagination, get_paginated_response_context
from src.account.selectors.technician_service_card import search_technician_service_card
from src.account.serializers.technician.technician_own_service_card import OutputTechnicianOwnServiceCardSerializer


class TechnicianOwnServiceCardListApi(IsTechnicianMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        summary="Get Technician Own Service Card",
        responses=OutputTechnicianOwnServiceCardSerializer)
    def get(self, request):
        db_technician_service_card_list = search_technician_service_card(
            technician_id=request.user.id,
        )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutputTechnicianOwnServiceCardSerializer,
            queryset=db_technician_service_card_list,
            request=request,
            view=self,
        )



