from django.contrib.auth.models import Group
from channels.db import database_sync_to_async
from django.db.models import Q
from src.authentication.models import User
from src.chat.models import ChatRoom, ChatMembership, ChatMessage
from src.chat.selectors.message import get_message_by_id, calculate_unread_messages
from src.service.models import Service
from src.authentication.selectors.auth import get_user
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


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
        logger.error(f"Error fetching technician services for user {user_id}: {str(e)}")
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
def _get_sender_information(user_id: str, base_url: Optional[str] = None) -> Optional[dict[str, str]]:
    """
    Get sender information for a user.
    Args:
        user_id: ID of the user.
        base_url: Optional base URL to construct absolute avatar URL.
    Returns:
        Dictionary with sender details or None if user not found.
    """
    try:
        user = get_user(id=user_id)
        if not user:
            logger.warning(f"User {user_id} not found in _get_sender_information")
            return None
        avatar = None
        full_name = ''
        if hasattr(user, 'profile') and user.profile:
            full_name = user.profile.full_name or ''
            if user.profile.avatar:
                avatar = f"{base_url}{user.profile.avatar.url}" if base_url else user.profile.avatar.url
        else:
            logger.warning(f"User {user_id} has no profile")
        return {
            "sender_id": str(user.id),
            "sender_role": (
                'TECHNICIAN' if user.groups.filter(name='TECHNICIAN').exists() else
                'ADMIN' if user.groups.filter(name='ADMIN').exists() else
                'SUPER_ADMIN' if user.groups.filter(name='SUPER_ADMIN').exists() else
                'UNKNOWN'
            ),
            "sender_full_name": full_name,
            "sender_avatar": avatar
        }
    except Exception as e:
        logger.error(f"Error in _get_sender_information for user {user_id}: {str(e)}")
        return None

async def format_message_payload(message_id: str, user_id: str, base_url: Optional[str] = None) -> dict:
    """
    Format the payload for a new message event.
    Args:
        message_id: ID of the message.
        user_id: ID of the user receiving the payload.
        base_url: Optional base URL to construct absolute URLs.
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
        sender_information = await _get_sender_information(str(message.user_id), base_url=base_url)
        if sender_information:
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
        logger.error(f"Error calculating unread messages for room {room_id} and user {user_id}: {str(e)}")
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

@database_sync_to_async
def _get_room_and_validate(room_id: str) -> Optional['ChatRoom']:
    """
    Get a room and validate it is a direct room.
    Args:
        room_id: ID of the room.
    Returns:
        ChatRoom instance or None if not found or invalid.
    """
    try:
        room = ChatRoom.objects.get(id=room_id)
        if room.type not in [ChatRoom.Type.TECHNICIAN_DIRECT, ChatRoom.Type.ADMIN_DIRECT]:
            logger.error(f"Room {room_id} is not a direct room")
            return None
        return room
    except ChatRoom.DoesNotExist:
        logger.error(f"Room {room_id} not found")
        return None

@database_sync_to_async
def _get_last_message(room_id: str, message_id: Optional[str] = None) -> Optional['ChatMessage']:
    """
    Get the last message for a room, using message_id if provided.
    Args:
        room_id: ID of the room.
        message_id: Optional ID of the message to retrieve directly.
    Returns:
        Last ChatMessage instance or None if not found.
    """
    try:
        if message_id:
            message = get_message_by_id(message_id=message_id)
            if message and str(message.room_id) == str(room_id):
                logger.debug(f"Retrieved message {message.id} for room {room_id} using message_id")
                return message
            else:
                logger.warning(f"Message {message_id} not found or not in room {room_id}")
        message = ChatMessage.objects.filter(room_id=room_id).order_by('-timestamp').first()
        if not message:
            logger.debug(f"No messages found for room {room_id}")
        else:
            logger.debug(f"Found last message {message.id} for room {room_id}")
        return message
    except Exception as e:
        logger.error(f"Failed to get last message for room {room_id}: {str(e)}")
        return None

@database_sync_to_async
def _get_counterpart_data(room_id: str, user_id: str, base_url: Optional[str] = None) -> Optional[dict]:
    """
    Get counterpart data for a direct room.
    Args:
        room_id: ID of the room.
        user_id: ID of the user.
        base_url: Optional base URL to construct absolute avatar URL.
    Returns:
        Dictionary with counterpart details or None if not found.
    """
    try:
        members = ChatMembership.objects.filter(
            room_id=room_id, left_at__isnull=True
        ).exclude(user_id=user_id)
        if not members.exists():
            logger.warning(f"No active members found for room {room_id} excluding user {user_id}")
            return None
        membership = members.first()
        counterpart_user = User.objects.get(id=membership.user_id)
        avatar = None
        full_name = ''
        if hasattr(counterpart_user, 'profile') and counterpart_user.profile:
            full_name = counterpart_user.profile.full_name or ''
            if counterpart_user.profile.avatar:
                avatar = f"{base_url}{counterpart_user.profile.avatar.url}" if base_url else counterpart_user.profile.avatar.url
        else:
            logger.warning(f"Counterpart user {membership.user_id} has no profile")
        return {
            'user_id': str(membership.user_id),
            'full_name': full_name,
            'avatar': avatar,
            'role': (
                'TECHNICIAN' if counterpart_user.groups.filter(name='TECHNICIAN').exists() else
                'ADMIN' if counterpart_user.groups.filter(name='ADMIN').exists() else
                'SUPER_ADMIN' if counterpart_user.groups.filter(name='SUPER_ADMIN').exists() else
                'UNKNOWN'
            )
        }
    except Exception as e:
        logger.error(f"Failed to get counterpart data for room {room_id}: {str(e)}")
        return None

async def format_new_room_payload(room_id: str, user_id: str, message_id: Optional[str] = None, base_url: Optional[str] = None) -> dict:
    """
    Format the payload for a new room event (TECHNICIAN_DIRECT, ADMIN_DIRECT).
    Args:
        room_id: ID of the room.
        user_id: ID of the user receiving the payload.
        message_id: Optional ID of the message to use as last_message.
        base_url: Optional base URL to construct absolute URLs.
    Returns:
        Formatted payload dictionary.
    """
    try:
        # Get and validate room
        room = await _get_room_and_validate(room_id)
        if not room:
            return {"error": "Room not found or not a direct room"}

        # Calculate unread messages
        unread_count = await _calculate_unread_messages(room_id, user_id)

        # Get last message, using provided message_id if available
        last_message = await _get_last_message(room_id, message_id)
        last_message_data = None
        if last_message:
            is_sent = str(last_message.user_id) == str(user_id) if last_message.user_id else False
            last_message_data = {
                'message_id': str(last_message.id),
                'text': last_message.text,
                'timestamp': last_message.timestamp.isoformat(),
                'is_sent': is_sent,
                'is_system_message': last_message.is_system_message,
                'sender': None
            }
            if last_message.user_id and not last_message.is_system_message:
                sender_info = await _get_sender_information(str(last_message.user_id), base_url=base_url)
                if sender_info:
                    last_message_data['sender'] = {
                        'full_name': sender_info['sender_full_name'],
                        'avatar': sender_info['sender_avatar'],
                        'role': sender_info['sender_role']
                    }

        # Prepare room data
        room_data = {
            'room_id': str(room.id),
            'type': room.type,
            'unread_messages_count': unread_count,
            'last_message': last_message_data,
            'counterpart': None,
            'service': None,
            'customer': None
        }

        # Add counterpart details
        counterpart_data = await _get_counterpart_data(room_id, user_id, base_url=base_url)
        if counterpart_data:
            room_data['counterpart'] = counterpart_data

        return room_data
    except Exception as e:
        logger.error(f"Failed to format new room payload for room {room_id}: {str(e)}")
        return {"error": str(("Failed to format room payload: %(error)s") % {"error": str(e)})}