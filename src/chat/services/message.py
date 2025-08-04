from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from src.chat.models import ChatMessage, ChatRoom, ChatMembership
from src.chat.selectors.message import get_message_by_id
from src.chat.services.room import get_or_create_room, add_members_to_room
from src.chat.services.cache import save_message_to_cache, update_message_in_cache
from src.chat.consumers.group_manager import add_room_members_to_group
from src.authentication.models import User
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def send_message(
        *,
        sender_id: str,
        service_id: Optional[str] = None,
        receiver_id: Optional[str] = None,
        text: Optional[str] = None,
        file_id: Optional[str] = None,
        replied_to_id: Optional[str] = None,
        room_id: Optional[str] = None
) -> ChatMessage:
    """
    Send a new user message to a chat room and ensure online members are added to the WebSocket group.
    Args:
        sender_id: ID of the sender.
        service_id: ID of the service for SERVICE rooms.
        receiver_id: ID of the receiver for direct rooms.
        text: Message text content.
        file_id: ID of the attached file, if any.
        replied_to_id: ID of the message being replied to, if any.
        room_id: Optional room ID provided by the client for new direct rooms.
    Returns:
        ChatMessage: The created message instance.
    Raises:
        ValidationError: If input validation fails.
    """
    logger.info(f"Attempting to send message from {sender_id} to receiver {receiver_id} with service_id {service_id}, room_id={room_id}")

    # Validate inputs
    if service_id and receiver_id:
        raise ValidationError(_("Cannot provide both service_id and receiver_id"))

    if not service_id and not receiver_id:
        raise ValidationError(_("Either service_id or receiver_id must be provided"))

    if not text and not file_id:
        raise ValidationError(_("Either text or file_id must be provided"))

    # Determine room type and validate users
    if service_id:
        room_type = ChatRoom.Type.SERVICE
        members_id = None
        if room_id:
            logger.error("room_id must be null for SERVICE rooms")
            raise ValidationError(_("room_id must be null for SERVICE rooms"))
        try:
            sender = User.objects.get(id=sender_id)
        except User.DoesNotExist:
            logger.error(f"Sender {sender_id} not found")
            raise ValidationError(_("Sender not found"))
    else:
        try:
            sender = User.objects.get(id=sender_id)
            receiver = User.objects.get(id=receiver_id)
            is_technician = (
                sender.groups.filter(name='TECHNICIAN').exists() or
                receiver.groups.filter(name='TECHNICIAN').exists()
            )
            room_type = ChatRoom.Type.TECHNICIAN_DIRECT if is_technician else ChatRoom.Type.ADMIN_DIRECT
            members_id = sorted([str(sender_id), str(receiver_id)])
        except User.DoesNotExist:
            logger.error(f"Sender {sender_id} or receiver {receiver_id} not found")
            raise ValidationError(_("Sender or receiver not found"))

    # Configure channel layer
    channel_layer = get_channel_layer()
    if channel_layer is None:
        logger.error("Channel layer is not configured")
        raise ValidationError(_("Channel layer is not configured"))

    # Get or create the room
    try:
        room, is_created = get_or_create_room(type=room_type, service_id=service_id, members_id=members_id, room_id=room_id)
        logger.info(f"Room {'created' if is_created else 'retrieved'}: {room.id}")
    except ValidationError as e:
        logger.error(f"Failed to get or create room: {str(e)}")
        raise ValidationError(_("Failed to get or create room: %(error)s") % {"error": str(e)})

    # Add sender to the room's membership for SERVICE rooms if not already a member
    if room_type == ChatRoom.Type.SERVICE:
        try:
            add_members_to_room(room_id=str(room.id), member_ids=[sender_id])
            logger.info(f"Sender {sender_id} added to room {room.id} if not already a member")
        except ValidationError as e:
            logger.error(f"Failed to add sender to room {room.id}: {str(e)}")
            raise ValidationError(_("Failed to add sender to room: %(error)s") % {"error": str(e)})

    # Add online members to the WebSocket group for new direct rooms or service rooms
    try:
        async_to_sync(add_room_members_to_group)(room)
        logger.info(f"Online members added to group room_{room.id}")
    except Exception as e:
        logger.warning(f"Failed to add members to group room_{room.id}: {str(e)}. Continuing as message will be saved.")

    # Validate replied-to message
    replied_to = None
    if replied_to_id:
        replied_to = get_message_by_id(message_id=replied_to_id)
        if not replied_to:
            logger.error(f"Replied-to message {replied_to_id} not found")
            raise ValidationError(_("Replied-to message not found"))

    # Create the message
    try:
        message = ChatMessage.objects.create(
            room_id=room.id,
            user_id=sender_id,
            text=text,
            file_id=file_id,
            replied_from_id=replied_to.id if replied_to else None,
            is_delivered=False,
            is_read=False,
            is_deleted=False,
            is_system_message=False
        )
        logger.info(f"Message created: {message.id}")
    except Exception as e:
        logger.error(f"Failed to create message: {str(e)}")
        raise ValidationError(_("Failed to create message: %(error)s") % {"error": str(e)})

    # Save to cache
    try:
        save_message_to_cache(message)
        logger.info(f"Message {message.id} saved to cache")
    except Exception as e:
        logger.error(f"Failed to save message to cache: {str(e)}")
        raise ValidationError(_("Failed to save message to cache: %(error)s") % {"error": str(e)})

    # Notify via WebSocket for new message
    group_name = f"room_{room.id}"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "chat_message",
            "message_id": str(message.id)
        }
    )
    logger.info(f"Message {message.id} sent to group {group_name}")

    # Notify receivers about unread message count (exclude sender)
    try:
        memberships = ChatMembership.objects.filter(
            room_id=room.id,
            left_at__isnull=True
        ).exclude(user_id=sender_id)
        for membership in memberships:
            async_to_sync(channel_layer.group_send)(
                f"user_{membership.user_id}",
                {
                    "type": "unread_message_count",
                    "room_id": str(room.id)
                }
            )
            logger.info(f"Unread count update sent to user {membership.user_id} for room {room.id}")
    except Exception as e:
        logger.warning(f"Failed to send unread count update for room {room.id}: {str(e)}")

    return message

def send_system_message(
        *,
        service_id: str,
        text: Optional[str] = None,
        file_id: Optional[str] = None,
        replied_to_id: Optional[str] = None
) -> ChatMessage:
    """
    Send a system message to a SERVICE room.
    Args:
        service_id: ID of the service for the SERVICE room.
        text: Message text content.
        file_id: ID of the attached file, if any.
        replied_to_id: ID of the message being replied to, if any.
    Returns:
        ChatMessage: The created system message instance.
    Raises:
        ValidationError: If input validation fails.
    """
    logger.info(f"Attempting to send system message for service_id {service_id}")

    if not service_id:
        logger.error("service_id is required for system messages")
        raise ValidationError(_("service_id is required for system messages"))

    # Get or create the SERVICE room
    try:
        room, is_created = get_or_create_room(type=ChatRoom.Type.SERVICE, service_id=service_id)
        logger.info(f"Room created or retrieved: {room.id}")
    except ValidationError as e:
        logger.error(f"Failed to get or create room: {str(e)}")
        raise ValidationError(_("Failed to get or create room: %(error)s") % {"error": str(e)})

    # Validate replied-to message
    replied_to = None
    if replied_to_id:
        replied_to = get_message_by_id(message_id=replied_to_id)
        if not replied_to:
            logger.error(f"Replied-to message {replied_to_id} not found")
            raise ValidationError(_("Replied-to message not found"))

    # Create the system message
    try:
        message = ChatMessage.objects.create(
            room_id=room.id,
            user_id=None,
            text=text,
            file_id=file_id,
            replied_from_id=replied_to.id if replied_to else None,
            is_delivered=False,
            is_read=False,
            is_deleted=False,
            is_system_message=True
        )
        logger.info(f"System message created: {message.id}")
    except Exception as e:
        logger.error(f"Failed to create system message: {str(e)}")
        raise ValidationError(_("Failed to create system message: %(error)s") % {"error": str(e)})

    # Save to cache
    try:
        save_message_to_cache(message)
        logger.info(f"System message {message.id} saved to cache")
    except Exception as e:
        logger.error(f"Failed to save system message to cache: {str(e)}")
        raise ValidationError(_("Failed to save message to cache: %(error)s") % {"error": str(e)})

    # Notify via WebSocket
    channel_layer = get_channel_layer()
    if channel_layer is None:
        logger.error("Channel layer is not configured")
        raise ValidationError(_("Channel layer is not configured"))

    group_name = f"room_{room.id}"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "chat_message",
            "message_id": str(message.id)
        }
    )
    logger.info(f"System message {message.id} sent to group {group_name}")

    # Notify all room members about unread message count
    try:
        memberships = ChatMembership.objects.filter(
            room_id=room.id,
            left_at__isnull=True
        )
        for membership in memberships:
            async_to_sync(channel_layer.group_send)(
                f"user_{membership.user_id}",
                {
                    "type": "unread_message_count",
                    "room_id": str(room.id)
                }
            )
            logger.info(f"Unread count update sent to user {membership.user_id} for room {room.id}")
    except Exception as e:
        logger.warning(f"Failed to send unread count update for room {room.id}: {str(e)}")

    return message

def mark_message_delivered(message_id: str, receiver_id: str) -> None:
    """
    Mark a message as delivered and notify room participants.
    Args:
        message_id: ID of the message to mark as delivered.
        receiver_id: ID of the user marking the message as delivered.
    Raises:
        ValidationError: If the message or room is invalid or user is unauthorized.
    """
    logger.info(f"Marking message {message_id} as delivered for receiver {receiver_id}")

    message = get_message_by_id(message_id=message_id)
    if not message:
        logger.error(f"Message {message_id} not found")
        raise ValidationError(_("Message not found"))

    try:
        room = ChatRoom.objects.get(id=message.room_id)
    except ChatRoom.DoesNotExist:
        logger.error(f"Room for message {message_id} not found")
        raise ValidationError(_("Room not found"))

    # Validate user authorization for SERVICE rooms
    if room.type == ChatRoom.Type.SERVICE:
        membership = ChatMembership.objects.filter(
            room_id=room.id,
            user_id=receiver_id,
            left_at__isnull=True
        ).first()
        if not membership:
            logger.error(f"User {receiver_id} not authorized to mark message {message_id} as delivered in SERVICE room")
            raise ValidationError(_("User not authorized to mark message as delivered"))

    if message.is_delivered:
        logger.info(f"Message {message_id} already delivered")
        return

    message.is_delivered = True
    message.save()
    logger.info(f"Message {message_id} marked as delivered")

    # Update cache
    try:
        update_message_in_cache(message)
        logger.info(f"Message {message_id} updated in cache")
    except Exception as e:
        logger.error(f"Failed to update message {message_id} in cache: {str(e)}")
        raise ValidationError(_("Failed to update message in cache: %(error)s") % {"error": str(e)})

    # Notify via WebSocket
    channel_layer = get_channel_layer()
    if channel_layer is None:
        logger.error("Channel layer is not configured")
        raise ValidationError(_("Channel layer is not configured"))

    group_name = f"room_{room.id}"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "message_status",
            "status": "delivered",
            "message_id": str(message.id)
        }
    )
    logger.info(f"Message status 'delivered' sent to group {group_name}")

def mark_message_read(message_id: str, user_id: str) -> None:
    """
    Mark a message as read and notify room participants.
    Args:
        message_id: ID of the message to mark as read.
        user_id: ID of the user marking the message as read.
    Raises:
        ValidationError: If the message or room is invalid or user is unauthorized.
    """
    logger.info(f"Marking message {message_id} as read for user {user_id}")

    message = get_message_by_id(message_id=message_id)
    if not message:
        logger.error(f"Message {message_id} not found")
        raise ValidationError(_("Message not found"))

    try:
        room = ChatRoom.objects.get(id=message.room_id)
    except ChatRoom.DoesNotExist:
        logger.error(f"Room for message {message_id} not found")
        raise ValidationError(_("Room not found"))

    # Validate user authorization for SERVICE rooms
    if room.type == ChatRoom.Type.SERVICE:
        membership = ChatMembership.objects.filter(
            room_id=room.id,
            user_id=user_id,
            left_at__isnull=True
        ).first()
        if not membership:
            logger.error(f"User {user_id} not authorized to mark message {message_id} as read in SERVICE room")
            raise ValidationError(_("User not authorized to mark message as read"))

    if message.is_read:
        logger.info(f"Message {message_id} already read")
        return

    message.is_read = True
    message.read_at = timezone.now()
    message.save()
    logger.info(f"Message {message_id} marked as read")

    # Update cache
    try:
        update_message_in_cache(message)
        logger.info(f"Message {message_id} updated in cache")
    except Exception as e:
        logger.error(f"Failed to update message {message_id} in cache: {str(e)}")
        raise ValidationError(_("Failed to update message in cache: %(error)s") % {"error": str(e)})

    # Notify via WebSocket for message status
    channel_layer = get_channel_layer()
    if channel_layer is None:
        logger.error("Channel layer is not configured")
        raise ValidationError(_("Channel layer is not configured"))

    group_name = f"room_{room.id}"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "message_status",
            "status": "read",
            "message_id": str(message.id)
        }
    )
    logger.info(f"Message status 'read' sent to group {group_name}")

    # Notify the user about updated unread message count
    try:
        async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
            {
                "type": "unread_message_count",
                "room_id": str(room.id)
            }
        )
        logger.info(f"Unread count update sent to user {user_id} for room {room.id}")
    except Exception as e:
        logger.warning(f"Failed to send unread count update for user {user_id} in room {room.id}: {str(e)}")