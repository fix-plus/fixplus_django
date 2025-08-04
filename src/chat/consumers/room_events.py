from channels.db import database_sync_to_async
from django.utils.translation import gettext_lazy as _
from src.chat.models import ChatRoom, ChatMembership
from src.chat.consumers.event_schema import NewRoomEvent
from src.chat.consumers.utils import format_new_room_payload
from typing import Any
import json
import logging

logger = logging.getLogger(__name__)


async def handle_new_room(consumer: Any, data: NewRoomEvent) -> None:
    """
    Handle the new_room event for direct rooms (TECHNICIAN_DIRECT, ADMIN_DIRECT).
    Args:
        consumer: The WebSocket consumer instance.
        data: The event data containing room_id.
    """
    try:
        room_id = data.get("room_id")
        logger.info(f"Handling new_room event for room_id={room_id} for user {consumer.user.id}")

        # Verify room exists and user is a member
        room = await database_sync_to_async(ChatRoom.objects.get)(id=room_id)
        if room.type not in [ChatRoom.Type.TECHNICIAN_DIRECT, ChatRoom.Type.ADMIN_DIRECT]:
            logger.error(f"Room {room_id} is not a direct room")
            raise ValueError(_("Room is not a direct room"))

        membership = await database_sync_to_async(ChatMembership.objects.filter)(
            room_id=room_id, user_id=consumer.user.id, left_at__isnull=True
        ).first()
        if not membership:
            logger.error(f"User {consumer.user.id} is not a member of room {room_id}")
            raise ValueError(_("User is not a member of the room"))

        # Format payload
        payload = await format_new_room_payload(room_id, str(consumer.user.id))
        await consumer.send(text_data=json.dumps({
            "type": "new_room",
            **payload
        }, ensure_ascii=False))
        logger.info(f"Sent new_room event to user {consumer.user.id} for room {room_id}")
    except ChatRoom.DoesNotExist:
        logger.error(f"Room {room_id} not found")
        await consumer.send(text_data=json.dumps({
            "type": "error",
            "error": str(_("Room not found"))
        }, ensure_ascii=False))
    except Exception as e:
        logger.error(f"Failed to handle new_room event: {str(e)}")
        await consumer.send(text_data=json.dumps({
            "type": "error",
            "error": str(_("Failed to process new room: %(error)s") % {"error": str(e)})
        }, ensure_ascii=False))