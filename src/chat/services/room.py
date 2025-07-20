import uuid
from typing import Tuple, Optional, List
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from src.authentication.models import User
from src.chat.models import ChatRoom, ChatMembership
import logging

logger = logging.getLogger(__name__)

def get_or_create_room(
        *,
        type: str,
        service_id: Optional[str] = None,
        members_id: Optional[List[str]] = None
) -> Tuple[ChatRoom, bool]:
    """
    Get or create a chat room based on the provided parameters.

    Args:
        type: Type of the room ('SERVICE', 'TECHNICIAN_DIRECT', 'ADMIN_DIRECT').
        service_id: ID of the service for SERVICE rooms (required for SERVICE rooms).
        members_id: Sorted list of user IDs for direct rooms (required for direct rooms).

    Returns:
        Tuple[ChatRoom, bool]: A tuple containing the existing or newly created chat room
                              and a boolean indicating if the room was created.

    Raises:
        ValidationError: If input validation fails, with translated error messages.
    """
    logger.info(f"Attempting to get or create room with type={type}, service_id={service_id}, members_id={members_id}")

    # Validate room type
    if type not in [ChatRoom.Type.SERVICE, ChatRoom.Type.TECHNICIAN_DIRECT, ChatRoom.Type.ADMIN_DIRECT]:
        logger.error(f"Invalid room type: {type}")
        raise ValidationError(_("Invalid room type: %(type)s") % {"type": type})

    # Handle SERVICE rooms
    if type == ChatRoom.Type.SERVICE:
        if not service_id:
            logger.error("service_id is required for SERVICE rooms")
            raise ValidationError(_("service_id is required for SERVICE rooms"))
        if members_id:
            logger.error("members_id must be null for SERVICE rooms")
            raise ValidationError(_("members_id must be null for SERVICE rooms"))

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

    # Handle direct rooms (TECHNICIAN_DIRECT or ADMIN_DIRECT)
    if not members_id:
        logger.error("members_id is required for direct rooms")
        raise ValidationError(_("members_id is required for direct rooms"))
    if service_id:
        logger.error("service_id must be null for direct rooms")
        raise ValidationError(_("service_id must be null for direct rooms"))
    if len(members_id) != 2:
        logger.error(f"Exactly two members are required for direct rooms, got {len(members_id)}")
        raise ValidationError(_("Exactly two members are required for direct rooms"))

    # Validate members_id and convert to strings
    members_id = [str(member_id) for member_id in members_id]
    for member_id in members_id:
        try:
            User.objects.get(id=member_id)
        except User.DoesNotExist:
            logger.error(f"User with ID {member_id} not found")
            raise ValidationError(_("User with ID %(id)s not found") % {"id": member_id})

    # Check for existing room with exactly these two members
    try:
        # Find rooms where the first member is present
        first_member_memberships = ChatMembership.objects.filter(
            user_id=members_id[0],
            left_at__isnull=True
        ).values_list('room_id', flat=True)

        logger.debug(f"Found {len(first_member_memberships)} rooms for user {members_id[0]}: {list(first_member_memberships)}")

        # Check each room to see if it contains exactly the two members
        for room_id in first_member_memberships:
            try:
                room = ChatRoom.objects.get(id=room_id, type=type)
                room_members = ChatMembership.objects.filter(
                    room_id=room_id,
                    left_at__isnull=True
                ).values_list('user_id', flat=True)
                room_members = [str(member_id) for member_id in room_members]
                logger.debug(f"Checking room {room_id} with members {room_members}")
                if sorted(room_members) == sorted(members_id):
                    logger.info(f"Found existing direct room {room.id} for members {members_id}")
                    return room, False
            except ChatRoom.DoesNotExist:
                logger.warning(f"Room {room_id} not found in ChatRoom, skipping")
                continue

        # Create new room if no matching room found
        room = ChatRoom.objects.create(
            type=type,
            service_id=None
        )
        logger.info(f"Created new direct room {room.id} with type {type}")

        # Create ChatMembership entries
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

        return room, True

    except Exception as e:
        logger.error(f"Failed to create or get direct room: {str(e)}")
        raise ValidationError(_("Failed to create or get direct room: %(error)s") % {"error": str(e)})