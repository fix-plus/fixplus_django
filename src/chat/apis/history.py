from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from src.chat.selectors.history import get_messages_history_list
from src.chat.serializers.history import OutputChatMessagesHistory
from src.common.mixins import IsVerifiedMobileMixin
from src.common.pagination import LimitOffsetPagination, get_paginated_response_context
from src.chat.models import ChatRoom, ChatMembership


class ChatMessageHistoryApi(IsVerifiedMobileMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 100

    @extend_schema(
        summary="Get Chat Message History for a Room",
        responses=OutputChatMessagesHistory,
    )
    def get(self, request, room_id):
        # Verify user is a member of the room
        membership = ChatMembership.objects.filter(
            room_id=room_id,
            user_id=request.user.id,
            left_at__isnull=True
        ).exists()
        if not membership:
            raise NotFound("Room not found or user is not a member")

        # Get message history
        queryset = get_messages_history_list(room_id=room_id)

        # Return paginated response
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutputChatMessagesHistory,
            queryset=queryset,
            request=request,
            view=self,
        )