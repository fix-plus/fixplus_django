from src.chat.models import ChatMessage, ChatRoom


def calculate_unread_messages(
        *,
        room_id: str,
        user_id: str,
):
    room = ChatRoom.objects.filter(id=room_id)

    if not room.exists():
        return 0

    count = ChatMessage.objects.filter(
        room_id=room.first().id,
        is_read=False,
    ).exclude(user_id=user_id).count()

    return count

def get_message_by_id(
        *,
        message_id: str = None,
) -> ChatMessage:
    try:
        return ChatMessage.objects.filter(id=message_id).first()
    except ChatMessage.DoesNotExist:
        raise ChatMessage.DoesNotExist()

def get_message_list_by_room(
        *,
        room_id: str,
):
    return ChatMessage.objects.filter(room_id=room_id).order_by("-timestamp")