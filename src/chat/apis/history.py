from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from src.chat.selectors.api import get_messages_history
from src.chat.serializers.message import OutputChatMessagesHistory
from src.common.mixins import IsVerifiedMixin
from src.common.pagination import LimitOffsetPagination, get_paginated_response_context
from src.user.selectors.auth import get_user


class ChatMessageHistoryApi(IsVerifiedMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 100

    @extend_schema(
        summary="Get Chat Message History",
        responses=OutputChatMessagesHistory,
    )
    def get(self, request, deal_offer_id):
        # Initialize
        user = request.user

        # Queryset
        queryset = get_messages_history(
            user=user,
            deal_offer_id=deal_offer_id,
        )

        # Response Pagination
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutputChatMessagesHistory,
            queryset=queryset,
            request=request,
            view=self,
        )