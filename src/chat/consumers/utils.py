from django.contrib.auth.models import Group
from channels.db import database_sync_to_async
from django.db.models import Q
from src.authentication.models import User
from src.chat.models import ChatRoom
from src.chat.selectors.message import get_message_by_id, calculate_unread_messages
from src.service.models import Service
from src.authentication.selectors.auth import get_user
from typing import List, Tuple, Optional

@database_sync_to_async
def get_users_services_id(user_id: str) -> List[dict]:
    """
    Get all service IDs associated with a user (admin or technician).
    Args:
        user_id: ID of the user.
    Returns:
        List of dictionaries containing service IDs.
    """
    try:
        user = User.objects.get(id=user_id)
        if user.groups.filter(Q(name='SUPER_ADMIN') | Q(name='ADMIN')).exists():
            return list(Service.objects.all().values('id'))
        return list(Service.objects.filter(technician__id=user_id).values('id'))
    except Exception as e:
        print(f"Error fetching technician services: {e}")
        return []

@database_sync_to_async
def _get_message_and_room(message_id: str) -> Tuple[Optional['ChatMessage'], Optional['ChatRoom']]:
    """
    Get a message and its associated room.
    Args:
        message_id: ID of the message.
    Returns:
        Tuple of (message, room) or (None, None) if not found.
    """
    try:
        message = get_message_by_id(message_id=message_id)
        if not message:
            return None, None
        room = ChatRoom.objects.get(id=message.room_id)
        return message, room
    except ChatRoom.DoesNotExist:
        return None, None

@database_sync_to_async
def _get_sender_information(user_id: str) -> Optional[dict[str, str]]:
    user = get_user(id=user_id)
    if not user:
        return None
    return {
        "sender_id": str(user.id),
        "sender_role": user.get_role(),
        "sender_full_name": user.profile.full_name,
        "sender_avatar": user.profile.avatar.url if user.profile.avatar else None
    }

async def format_message_payload(message_id: str, user_id: str) -> dict:
    """
    Format the payload for a new message event.
    Args:
        message_id: ID of the message.
        user_id: ID of the user receiving the payload.
    Returns:
        Formatted payload dictionary.
    """
    message, room = await _get_message_and_room(message_id)
    if not message or not room:
        return {"error": "Message or room not found"}

    is_sent = str(message.user_id) == str(user_id)

    message_data = {
        "id": str(message.id),
        "is_sent": is_sent,
        "text": message.text,
        "file_id": str(message.file_id) if message.file_id else None,
        "replied_from_id": str(message.replied_from_id) if message.replied_from_id else None,
        "is_system_message": message.is_system_message,
        "timestamp": int(message.timestamp.timestamp()),
    }

    if not is_sent and not message.is_system_message:
        sender_information = await _get_sender_information(str(message.user_id))
        message_data.update(sender_information)

    return {
        "room_id": str(room.id),
        "service_id": str(room.service_id) if room.service_id else None,
        "message": message_data
    }

async def format_status_payload(message_id: str, status: str) -> dict:
    """
    Format the payload for a message status event.
    Args:
        message_id: ID of the message.
        status: Status of the message (delivered, read).
    Returns:
        Formatted payload dictionary.
    """
    message, room = await _get_message_and_room(message_id)
    if not message or not room:
        return {"error": "Message or room not found"}

    return {
        "service_id": str(room.service_id) if room.service_id else None,
        "message_id": str(message_id),
        "status": status
    }

@database_sync_to_async
def _calculate_unread_messages(room_id: str, user_id: str) -> int:
    """
    Calculate the number of unread messages for a user in a room.
    Args:
        room_id: ID of the room.
        user_id: ID of the user.
    Returns:
        Number of unread messages.
    """
    try:
        return calculate_unread_messages(room_id=room_id, user_id=user_id)
    except Exception as e:
        print(f"Error calculating unread messages for room {room_id} and user {user_id}: {e}")
        return 0

async def format_unread_count_payload(room_id: str, user_id: str) -> dict:
    """
    Format the payload for an unread message count event.
    Args:
        room_id: ID of the room.
        user_id: ID of the user receiving the payload.
    Returns:
        Formatted payload dictionary.
    """
    unread_count = await _calculate_unread_messages(room_id, user_id)
    return {
        "room_id": room_id,
        "unread_count": unread_count
    }