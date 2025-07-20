import json
from django.utils.translation import gettext as _
from .utils import get_users_services_id
from channels.layers import get_channel_layer
from src.chat.models import ChatRoom, ChatMembership
from src.chat.services.channel_storage import channel_storage
from typing import Any, Optional, List
from asgiref.sync import async_to_sync, sync_to_async
import logging

logger = logging.getLogger(__name__)

async def get_direct_chat_groups(user_id: str) -> List[str]:
    """
    Retrieve direct chat group names for a given user based on ChatMembership.
    Args:
        user_id: ID of the user.
    Returns:
        List of group names (e.g., ['room_<room_id>', ...]) for direct chat rooms.
    """
    try:
        # Get memberships for the user
        memberships = await sync_to_async(
            lambda: list(ChatMembership.objects.filter(
                user_id=user_id,
                left_at__isnull=True
            ))
        )()
        logger.debug(f"Found {len(memberships)} memberships for user {user_id}")

        group_names = []
        for membership in memberships:
            try:
                # Get room type for each room_id
                room = await sync_to_async(
                    lambda: ChatRoom.objects.get(id=membership.room_id)
                )()
                if room.type in [ChatRoom.Type.TECHNICIAN_DIRECT, ChatRoom.Type.ADMIN_DIRECT]:
                    group_names.append(f"room_{membership.room_id}")
                    logger.debug(f"Added group room_{membership.room_id} for user {user_id}")
            except ChatRoom.DoesNotExist:
                logger.warning(f"Room {membership.room_id} not found for user {user_id}, skipping")
                continue

        logger.debug(f"Retrieved direct chat groups for user {user_id}: {group_names}")
        return group_names
    except Exception as e:
        logger.error(f"Error fetching direct chat groups for user {user_id}: {str(e)}")
        raise  # Re-raise the exception to be handled by the caller

async def join_user_groups(consumer: Any) -> None:
    """
    Add consumer to relevant WebSocket groups (user, service, and direct chat).
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

    # Join user-specific group
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

    # Join service groups
    try:
        services = await get_users_services_id(consumer.user.id)
        consumer.service_groups = [f"service_{service['id']}" for service in services]
        for group in consumer.service_groups:
            await channel_layer.group_add(group, consumer.channel_name)
            logger.info(f"User {consumer.user.id} added to service group {group}")
    except Exception as e:
        logger.error(f"Failed to join service groups for user {consumer.user.id}: {str(e)}")
        await consumer.send(text_data=json.dumps({
            "type": "error",
            "error": str(_("Failed to join service groups: %(error)s") % {"error": str(e)})
        }, ensure_ascii=False))
        return

    # Join direct chat groups
    try:
        consumer.direct_groups = await get_direct_chat_groups(str(consumer.user.id))
        for group in consumer.direct_groups:
            await channel_layer.group_add(group, consumer.channel_name)
            logger.info(f"User {consumer.user.id} added to direct chat group {group}")
    except Exception as e:
        logger.error(f"Failed to join direct chat groups for user {consumer.user.id}: {str(e)}")
        await consumer.send(text_data=json.dumps({
            "type": "error",
            "error": str(_("Failed to join direct chat groups: %(error)s") % {"error": str(e)})
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

    # Leave user-specific group
    if hasattr(consumer, 'user_group_name') and consumer.user_group_name:
        await channel_layer.group_discard(consumer.user_group_name, consumer.channel_name)
        logger.info(f"User {consumer.user.id} removed from group {consumer.user_group_name}")

    # Leave service groups
    for group in getattr(consumer, "service_groups", []):
        await channel_layer.group_discard(group, consumer.channel_name)
        logger.info(f"User {consumer.user.id} removed from service group {group}")

    # Leave direct chat groups
    for group in getattr(consumer, "direct_groups", []):
        await channel_layer.group_discard(group, consumer.channel_name)
        logger.info(f"User {consumer.user.id} removed from direct chat group {group}")

def add_room_members_to_group(room: ChatRoom, exclude_user_id: Optional[str] = None) -> None:
    """
    Add all online room members to the WebSocket group for the given room.
    Args:
        room: The ChatRoom instance.
        exclude_user_id: Optional user ID to exclude from adding to the group.
    """
    channel_layer = get_channel_layer()
    if channel_layer is None:
        logger.error("Channel layer is not configured")
        return

    if room.type not in [ChatRoom.Type.TECHNICIAN_DIRECT, ChatRoom.Type.ADMIN_DIRECT]:
        logger.debug(f"Skipping group add for room {room.id} (type {room.type} is not direct)")
        return

    group_name = f"room_{room.id}"
    try:
        # Use sync_to_async for database queries in async context
        memberships = sync_to_async(
            lambda: list(ChatMembership.objects.filter(room_id=room.id, left_at__isnull=True))
        )()
        for membership in memberships:
            member_id = str(membership.user_id)
            if member_id != exclude_user_id:
                channel_name = channel_storage.get_channel_name(member_id)
                if channel_name:
                    try:
                        async_to_sync(channel_layer.group_add)(group_name, channel_name)
                        logger.info(f"User {member_id} added to group {group_name} with channel {channel_name}")
                    except Exception as e:
                        logger.warning(f"Failed to add user {member_id} to group {group_name}: {str(e)}")
                else:
                    logger.debug(f"User {member_id} is offline, skipping group add for {group_name}")
    except Exception as e:
        logger.error(f"Failed to fetch memberships for room {room.id}: {str(e)}")