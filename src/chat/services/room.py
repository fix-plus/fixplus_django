import uuid
from typing import Tuple, Optional, List
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from src.authentication.models import User
from src.chat.models import ChatRoom, ChatMembership
from src.chat.consumers.group_manager import add_room_members_to_group, remove_member_from_group
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import logging

logger = logging.getLogger(__name__)

def get_or_create_service_room(service_id: str) -> Tuple[ChatRoom, bool]:
    """
    Get or create a SERVICE room for a given service ID.
    Args:
        service_id: ID of the service.
    Returns:
        Tuple[ChatRoom, bool]: A tuple containing the existing or newly created SERVICE room
                              and a boolean indicating if the room was created.
    Raises:
        ValidationError: If the room creation fails or input validation fails.
    """
    logger.info(f"Attempting to get or create SERVICE room for service_id={service_id}")

    if not service_id:
        logger.error("service_id is required for SERVICE rooms")
        raise ValidationError(_("service_id is required for SERVICE rooms"))

    try:
        room, created = ChatRoom.objects.get_or_create(
            type=ChatRoom.Type.SERVICE,
            service_id=service_id,
        )
        logger.info(f"SERVICE room {'created' if created else 'retrieved'}: {room.id} for service_id={service_id}")
        return room, created
    except Exception as e:
        logger.error(f"Failed to get or create SERVICE room for service_id={service_id}: {str(e)}")
        raise ValidationError(_("Failed to get or create SERVICE room: %(error)s") % {"error": str(e)})

def add_members_to_room(room_id: str, member_ids: List[str]) -> List[ChatMembership]:
    """
    Add members to a room with active memberships and update WebSocket groups.
    If a member was previously in the room and left, a new membership is created.
    Args:
        room_id: ID of the room.
        member_ids: List of user IDs to add as members.
    Returns:
        List[ChatMembership]: List of created or updated membership instances.
    Raises:
        ValidationError: If validation fails or users/rooms are not found.
    """
    logger.info(f"Adding members {member_ids} to room {room_id}")

    try:
        room = ChatRoom.objects.get(id=room_id)
    except ChatRoom.DoesNotExist:
        logger.error(f"Room {room_id} not found")
        raise ValidationError(_("Room not found"))

    memberships = []
    for member_id in member_ids:
        try:
            User.objects.get(id=member_id)
        except User.DoesNotExist:
            logger.error(f"User {member_id} not found")
            raise ValidationError(_("User with ID %(id)s not found") % {"id": member_id})

        existing_membership = ChatMembership.objects.filter(
            room_id=room_id,
            user_id=member_id,
            left_at__isnull=True
        ).first()

        if not existing_membership:
            membership = ChatMembership.objects.create(
                room_id=room_id,
                user_id=member_id,
                joined_at=timezone.now()
            )
            logger.info(f"Created ChatMembership for user {member_id} in room {room_id}")
            memberships.append(membership)
        else:
            logger.debug(f"User {member_id} already has active membership in room {room_id}")
            memberships.append(existing_membership)

    # Update WebSocket group for all active members
    try:
        async_to_sync(add_room_members_to_group)(room)
        logger.info(f"Updated WebSocket group for room {room_id} with all active members")
    except Exception as e:
        logger.warning(f"Failed to update WebSocket group for room {room_id}: {str(e)}. Memberships created successfully.")

    return memberships

def remove_member_from_room(room_id: str, member_id: str) -> None:
    """
    Remove a member from a room by setting left_at and update WebSocket group.
    Args:
        room_id: ID of the room.
        member_id: ID of the user to remove.
    Raises:
        ValidationError: If the membership or room is not found.
    """
    logger.info(f"Removing member {member_id} from room {room_id}")

    try:
        room = ChatRoom.objects.get(id=room_id)
    except ChatRoom.DoesNotExist:
        logger.error(f"Room {room_id} not found")
        raise ValidationError(_("Room not found"))

    try:
        User.objects.get(id=member_id)
    except User.DoesNotExist:
        logger.error(f"User {member_id} not found")
        raise ValidationError(_("User with ID %(id)s not found") % {"id": member_id})

    membership = ChatMembership.objects.filter(
        room_id=room_id,
        user_id=member_id,
        left_at__isnull=True
    ).first()

    if not membership:
        logger.warning(f"No active membership found for user {member_id} in room {room_id}")
        raise ValidationError(_("No active membership found for user in room"))

    membership.left_at = timezone.now()
    membership.save()
    logger.info(f"User {member_id} removed from room {room_id} by setting left_at")

    # Remove user from WebSocket group
    try:
        async_to_sync(remove_member_from_group)(room, member_id)
        logger.info(f"User {member_id} removed from WebSocket group for room {room_id}")
    except Exception as e:
        logger.warning(f"Failed to remove user {member_id} from WebSocket group for room {room_id}: {str(e)}")

def get_or_create_room(
        *,
        type: str,
        service_id: Optional[str] = None,
        members_id: Optional[List[str]] = None,
        room_id: Optional[str] = None,
        send_event: bool = True
) -> Tuple[ChatRoom, bool]:
    """
    Get or create a chat room based on the provided parameters and notify members.
    Args:
        type: Type of the room ('SERVICE', 'TECHNICIAN_DIRECT', 'ADMIN_DIRECT').
        service_id: ID of the service for SERVICE rooms.
        members_id: Sorted list of user IDs for direct rooms.
        room_id: Optional room ID provided by the client for new rooms, mandatory for new direct rooms.
        send_event: Whether to send the new_room event to members (default: True).
    Returns:
        Tuple[ChatRoom, bool]: A tuple containing the existing or newly created chat room
                              and a boolean indicating if the room was created.
    Raises:
        ValidationError: If input validation fails.
    """
    logger.info(f"Attempting to get or create room with type={type}, service_id={service_id}, members_id={members_id}, room_id={room_id}, send_event={send_event}")

    if type not in [ChatRoom.Type.SERVICE, ChatRoom.Type.TECHNICIAN_DIRECT, ChatRoom.Type.ADMIN_DIRECT]:
        logger.error(f"Invalid room type: {type}")
        raise ValidationError(_("Invalid room type: %(type)s") % {"type": type})

    channel_layer = get_channel_layer()
    if channel_layer is None:
        logger.error("Channel layer is not configured")
        raise ValidationError(_("Channel layer is not configured"))

    if type == ChatRoom.Type.SERVICE:
        if not service_id:
            logger.error("service_id is required for SERVICE rooms")
            raise ValidationError(_("service_id is required for SERVICE rooms"))
        if members_id:
            logger.error("members_id must be null for SERVICE rooms")
            raise ValidationError(_("members_id must be null for SERVICE rooms"))
        if room_id:
            logger.error("room_id must be null for SERVICE rooms")
            raise ValidationError(_("room_id must be null for SERVICE rooms"))

        try:
            room, created = ChatRoom.objects.get_or_create(
                type=ChatRoom.Type.SERVICE,
                service_id=service_id,
            )
            logger.info(f"SERVICE room {'created' if created else 'retrieved'}: {room.id}")
            return room, created
        except Exception as e:
            logger.error(f"Failed to create or get SERVICE room: {str(e)}")
            raise ValidationError(_("Failed to create or get SERVICE room: %(error)s") % {"error": str(e)})

    if not members_id:
        logger.error("members_id is required for direct rooms")
        raise ValidationError(_("members_id is required for direct rooms"))
    if service_id:
        logger.error("service_id must be null for direct rooms")
        raise ValidationError(_("service_id must be null for direct rooms"))
    if len(members_id) != 2:
        logger.error(f"Exactly two members are required for direct rooms, got {len(members_id)}")
        raise ValidationError(_("Exactly two members are required for direct rooms"))

    members_id = [str(member_id) for member_id in members_id]
    for member_id in members_id:
        try:
            User.objects.get(id=member_id)
        except User.DoesNotExist:
            logger.error(f"User with ID {member_id} not found")
            raise ValidationError(_("User with ID %(id)s not found") % {"id": member_id})

    try:
        # Check if a room already exists for the given members
        first_member_memberships = ChatMembership.objects.filter(
            user_id=members_id[0],
            left_at__isnull=True
        ).values_list('room_id', flat=True)

        logger.debug(f"Found {len(first_member_memberships)} rooms for user {members_id[0]}: {list(first_member_memberships)}")

        for existing_room_id in first_member_memberships:
            try:
                room = ChatRoom.objects.get(id=existing_room_id, type=type)
                room_members = ChatMembership.objects.filter(
                    room_id=existing_room_id,
                    left_at__isnull=True
                ).values_list('user_id', flat=True)
                room_members = [str(member_id) for member_id in room_members]
                logger.debug(f"Checking room {existing_room_id} with members {room_members}")
                if sorted(room_members) == sorted(members_id):
                    logger.info(f"Found existing direct room {room.id} for members {members_id}")
                    return room, False
            except ChatRoom.DoesNotExist:
                logger.warning(f"Room {existing_room_id} not found in ChatRoom, skipping")
                continue

        # For new direct rooms, room_id is mandatory
        if not room_id:
            logger.error("room_id is required for creating new direct rooms")
            raise ValidationError(_("room_id is required for creating new direct rooms"))

        # Validate provided room_id
        try:
            uuid.UUID(room_id)  # Validate that room_id is a valid UUID
            if ChatRoom.objects.filter(id=room_id).exists():
                logger.error(f"Room with ID {room_id} already exists")
                raise ValidationError(_("Room with provided ID already exists"))
        except ValueError:
            logger.error(f"Invalid room_id format: {room_id}")
            raise ValidationError(_("Invalid room_id format"))

        # Create new room with provided room_id
        room = ChatRoom.objects.create(
            id=room_id,  # Use provided room_id
            type=type,
            service_id=None
        )
        logger.info(f"Created new direct room {room.id} with type {type}")

        for member_id in members_id:
            membership, created = ChatMembership.objects.get_or_create(
                room_id=room.id,
                user_id=member_id,
                defaults={'joined_at': timezone.now()}
            )
            if created:
                logger.info(f"Created ChatMembership for user {member_id} in room {room.id}")
            else:
                logger.debug(f"ChatMembership for user {member_id} in room {room.id} already exists")

        # Update WebSocket group for new room
        try:
            async_to_sync(add_room_members_to_group)(room)
            logger.info(f"Updated WebSocket group for new room {room.id}")
        except Exception as e:
            logger.warning(f"Failed to update WebSocket group for room {room.id}: {str(e)}. Memberships created successfully.")

        # Notify members about new room if send_event is True
        if send_event:
            try:
                group_name = f"room_{room.id}"
                async_to_sync(channel_layer.group_send)(
                    group_name,
                    {
                        "type": "new_room",
                        "room_id": str(room.id)
                    }
                )
                logger.info(f"Sent new_room event to group {group_name}")
            except Exception as e:
                logger.warning(f"Failed to send new_room event for room {room.id}: {str(e)}")

        return room, True

    except Exception as e:
        logger.error(f"Failed to create or get direct room: {str(e)}")
        raise ValidationError(_("Failed to create or get direct room: %(error)s") % {"error": str(e)})