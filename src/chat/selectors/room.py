from src.chat.models import ChatRoom


def get_room(
        *,
        type: str,
        users_id :list = None,
        service_id :str = None,
):
    room = ChatRoom.objects.filter(type=type)

    if users_id:
        room = room.filter(members__id=users_id)
    elif service_id:
        room = room.filter(service_id=service_id)
    else:
        return ChatRoom.objects.none()

    return room