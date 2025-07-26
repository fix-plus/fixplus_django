import json
from django.utils.translation import gettext as _
from channels.layers import get_channel_layer
from src.chat.models import ChatRoom, ChatMembership
from src.chat.services.channel_storage import channel_storage
from typing import Any, Optional, List
from asgiref.sync import sync_to_async
import logging

logger = logging.getLogger(__name__)

async def get_direct_chat_groups(user_id: str) -> List[str]:
    """
    Retrieve chat group names for a given user based on active ChatMembership.
    Args:
        user_id: ID of the user.
    Returns:
        List of group names (e.g., ['room_<room_id>', ...] for all room types).
    """
    try:
        memberships = await sync_to_async(
            lambda: list(ChatMembership.objects.filter(
                user_id=user_id,
                left_at__isnull=True
            ).values_list('room_id', flat=True))
        )()
        logger.debug(f"Found {len(memberships)} active memberships for user {user_id}")

        group_names = []
        rooms = await sync_to_async(
            lambda: list(ChatRoom.objects.filter(
                id__in=memberships,
                type__in=[
                    ChatRoom.Type.SERVICE,
                    ChatRoom.Type.TECHNICIAN_DIRECT,
                    ChatRoom.Type.ADMIN_DIRECT
                ]
            ).values('id', 'type', 'service_id'))
        )()

        for room in rooms:
            # Use room_id for all room types to ensure consistency
            group_name = f"room_{room['id']}"
            if group_name not in group_names:
                group_names.append(group_name)
                logger.debug(f"Added group {group_name} for user {user_id}")

        logger.debug(f"Retrieved chat groups for user {user_id}: {group_names}")
        return group_names
    except Exception as e:
        logger.error(f"Error fetching chat groups for user {user_id}: {str(e)}")
        raise

async def join_user_groups(consumer: Any) -> None:
    """
    Add consumer to relevant WebSocket groups (user, service, and chat rooms).
    Args:
        consumer: The WebSocket consumer instance.
    """
    channel_layer = get_channel_layer()
    if channel_layer is None:
        logger.error("Channel layer is not configured")
        await consumer.send(text_data=json.dumps({
            "type": "error",
            "error": str(_("Channel layer is not configured"))
        }, ensure_ascii=False))
        raise RuntimeError("Channel layer is not configured")

    # Add user to their personal group
    try:
        consumer.user_group_name = f"user_{consumer.user.id}"
        await channel_layer.group_add(consumer.user_group_name, consumer.channel_name)
        logger.info(f"User {consumer.user.id} added to group {consumer.user_group_name}")
    except Exception as e:
        logger.error(f"Failed to join user group for user {consumer.user.id}: {str(e)}")
        await consumer.send(text_data=json.dumps({
            "type": "error",
            "error": str(_("Failed to join user group: %(error)s") % {"error": str(e)})
        }, ensure_ascii=False))
        return

    # Add user to service and direct chat groups
    try:
        consumer.direct_groups = await get_direct_chat_groups(str(consumer.user.id))
        for group in consumer.direct_groups:
            await channel_layer.group_add(group, consumer.channel_name)
            logger.info(f"User {consumer.user.id} added to group {group}")
    except Exception as e:
        logger.error(f"Failed to join chat groups for user {consumer.user.id}: {str(e)}")
        await consumer.send(text_data=json.dumps({
            "type": "error",
            "error": str(_("Failed to join chat groups: %(error)s") % {"error": str(e)})
        }, ensure_ascii=False))
        return

async def leave_user_groups(consumer: Any) -> None:
    """
    Remove consumer from all WebSocket groups and cache.
    Args:
        consumer: The WebSocket consumer instance.
    """
    channel_layer = get_channel_layer()
    if channel_layer is None:
        logger.error("Channel layer is not configured")
        return

    if hasattr(consumer, 'user_group_name') and consumer.user_group_name:
        await channel_layer.group_discard(consumer.user_group_name, consumer.channel_name)
        logger.info(f"User {consumer.user.id} removed from group {consumer.user_group_name}")

    for group in getattr(consumer, "direct_groups", []):
        await channel_layer.group_discard(group, consumer.channel_name)
        logger.info(f"User {consumer.user.id} removed from group {group}")

async def add_room_members_to_group(room: ChatRoom, exclude_user_ids: Optional[List[str]] = None) -> None:
    """
    Add all online room members to the WebSocket group for the given room.
    Args:
        room: The ChatRoom instance.
        exclude_user_ids: Optional list of user IDs to exclude from adding to the group.
    """
    channel_layer = get_channel_layer()
    if channel_layer is None:
        logger.error("Channel layer is not configured")
        return

    if room.type not in [ChatRoom.Type.SERVICE, ChatRoom.Type.TECHNICIAN_DIRECT, ChatRoom.Type.ADMIN_DIRECT]:
        logger.debug(f"Skipping group add for room {room.id} (type {room.type} is not valid)")
        return

    group_name = f"room_{room.id}"
    exclude_user_ids = set(exclude_user_ids or [])  # Convert to set for O(1) lookup
    try:
        memberships = await sync_to_async(
            lambda: list(ChatMembership.objects.filter(
                room_id=room.id,
                left_at__isnull=True
            ))
        )()
        for membership in memberships:
            member_id = str(membership.user_id)
            if member_id not in exclude_user_ids:
                channel_name = channel_storage.get_channel_name(member_id)
                if channel_name:
                    try:
                        await channel_layer.group_add(group_name, channel_name)
                        logger.info(f"User {member_id} added to group {group_name} with channel {channel_name}")
                    except Exception as e:
                        logger.warning(f"Failed to add user {member_id} to group {group_name}: {str(e)}")
                else:
                    logger.debug(f"User {member_id} is offline, skipping group add for {group_name}")
    except Exception as e:
        logger.error(f"Failed to fetch memberships for room {room.id}: {str(e)}")
        raise

async def remove_member_from_group(room: ChatRoom, member_id: str) -> None:
    """
    Remove a member from the WebSocket group for the given room.
    Args:
        room: The ChatRoom instance.
        member_id: ID of the user to remove from the group.
    """
    channel_layer = get_channel_layer()
    if channel_layer is None:
        logger.error("Channel layer is not configured")
        return

    group_name = f"room_{room.id}"
    channel_name = channel_storage.get_channel_name(member_id)
    if channel_name:
        try:
            await channel_layer.group_discard(group_name, channel_name)
            logger.info(f"User {member_id} removed from group {group_name} with channel {channel_name}")
        except Exception as e:
            logger.warning(f"Failed to remove user {member_id} from group {group_name}: {str(e)}")
    else:
        logger.debug(f"User {member_id} is offline, no need to remove from group {group_name}")