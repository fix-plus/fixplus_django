from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from src.chat.selectors.counterpart_user import get_counterpart_user
from src.chat.serializers.counterpart_user import OutputCounterpartUser, InputParamsCounterpartUser
from src.common.mixins import IsVerifiedMobileMixin
from src.common.pagination import LimitOffsetPagination, get_paginated_response_context


class ChatCounterpartUserApi(IsVerifiedMobileMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 100

    @extend_schema(
        summary="Get Counterpart User",
        parameters=[InputParamsCounterpartUser],
        responses=OutputCounterpartUser,
    )
    def get(self, request):
        serializer = InputParamsCounterpartUser(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        # Get message history
        queryset = get_counterpart_user(
            exclude_user_id=request.user.id,
            **serializer.validated_data,
        )

        # Return paginated response
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutputCounterpartUser,
            queryset=queryset,
            request=request,
            view=self,
        )