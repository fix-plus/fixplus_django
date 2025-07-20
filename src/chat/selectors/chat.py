from uuid import UUID

from src.authentication.models import User
from src.chat.models import ChatMessage, ChatRoom


def get_chat_room_list(
        *,
        user: User,
        room_type: str,
):
    room = None

    if room_type == ChatRoom.Type.SERVICE:
        room = ChatRoom.objects.filter(
            type=ChatRoom.Type.SERVICE,
            members_id__contains=[str(user.id)]
        ).first()
    elif room_type == ChatRoom.Type.TECHNICIAN_DIRECT:
        room = ChatRoom.objects.filter(
            type=ChatRoom.Type.TECHNICIAN_DIRECT,
            members_id__contains=[str(user.id)]
        ).first()
    elif room_type == ChatRoom.Type.ADMIN_DIRECT:
        room = ChatRoom.objects.filter(
            type=ChatRoom.Type.ADMIN_DIRECT,
            members_id__contains=[str(user.id)]
        ).first()

