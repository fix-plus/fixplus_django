from src.chat.models import ChatMessage, ChatRoom


def get_messages_history_list(
        *,
        room_id: str,
):
    room = ChatRoom.objects.filter(id=room_id)

    if not room.exists():
        return ChatMessage.objects.none()

    queryset = ChatMessage.objects.filter(
        room_id=room.first().id,
    )

    return queryset.order_by('-timestamp')