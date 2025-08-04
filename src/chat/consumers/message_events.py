from typing import Any

from channels.db import database_sync_to_async
from django.utils.translation import gettext_lazy as _
from src.chat.services.message import send_message
from src.chat.consumers.event_schema import SendMessageEvent
from src.chat.models import ChatRoom
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import logging

logger = logging.getLogger(__name__)

async def handle_send_message(consumer: Any, data: SendMessageEvent) -> None:
    """
    Handle the send_message event.
    Args:
        consumer: The WebSocket consumer instance.
        data: The event data containing message details.
    """
    try:
        # Check if the room is new by calling get_or_create_room
        room_id = data.get("room_id")
        created = False
        if data.get("receiver_id") and data.get("type") in [ChatRoom.Type.TECHNICIAN_DIRECT, ChatRoom.Type.ADMIN_DIRECT]:
            from .room import get_or_create_room
            room, created = await database_sync_to_async(get_or_create_room)(
                type=data.get("type"),
                members_id=[str(consumer.user.id), data.get("receiver_id")],
                room_id=room_id,
                send_event=False  # Prevent sending new_room event in get_or_create_room
            )
            room_id = str(room.id)  # Update room_id in case it was created

        # Send the message and get the message object
        message = await database_sync_to_async(send_message)(
            room_id=room_id,
            sender_id=str(consumer.user.id),
            service_id=data.get("service_id"),
            receiver_id=data.get("receiver_id"),
            text=data.get("text"),
            file_id=data.get("file_id"),
            replied_to_id=data.get("replied_to_id")
        )

        # If room was created, send new_room event to the group with message_id
        if created:
            channel_layer = get_channel_layer()
            if channel_layer is None:
                logger.error("Channel layer is not configured")
                raise RuntimeError("Channel layer is not configured")
            try:
                group_name = f"room_{room_id}"
                async_to_sync(channel_layer.group_send)(
                    group_name,
                    {
                        "type": "new_room",
                        "room_id": str(room_id),
                        "message_id": str(message.id)  # Pass message_id to ensure last_message is populated
                    }
                )
                logger.info(f"Sent new_room event to group {group_name} after message creation with message_id {message.id}")
            except Exception as e:
                logger.warning(f"Failed to send new_room event for room {room_id}: {str(e)}")

    except Exception as e:
        error_message = str(e).replace("['", "").replace("']", "")
        await consumer.send(text_data=json.dumps({
            "type": "error",
            "error": str(_(error_message))
        }, ensure_ascii=False))