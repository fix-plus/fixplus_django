from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from src.chat.selectors.chat import get_chat_room_list
from src.chat.serializers.chat import OutputChatRoomSerializer, InputParamsChatRoomSerializer
from src.common.mixins import IsVerifiedMobileMixin
from src.common.pagination import LimitOffsetPagination, get_paginated_response_context


class ChatRoomListApi(IsVerifiedMobileMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 100

    @extend_schema(
        summary="Get List of Chat Rooms",
        request=InputParamsChatRoomSerializer,
        responses=OutputChatRoomSerializer(many=True),
    )
    def get(self, request):
        # Validate input parameters
        serializer = InputParamsChatRoomSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        # Get chat rooms for the user
        queryset = get_chat_room_list(
            user=request.user,
            **serializer.validated_data,
        )

        # Return paginated response
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutputChatRoomSerializer,
            queryset=queryset,
            request=request,
            view=self,
        )