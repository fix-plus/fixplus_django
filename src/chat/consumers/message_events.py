from channels.db import database_sync_to_async
from django.utils.translation import gettext_lazy as _
from src.chat.services.message import send_message
from src.chat.consumers.event_schema import SendMessageEvent
from typing import Any
import json


async def handle_send_message(consumer: Any, data: SendMessageEvent) -> None:
    """
    Handle the send_message event.
    Args:
        consumer: The WebSocket consumer instance.
        data: The event data containing message details.
    """
    try:
        await database_sync_to_async(send_message)(
            room_id=data.get("room_id"),
            sender_id=str(consumer.user.id),
            service_id=data.get("service_id"),
            receiver_id=data.get("receiver_id"),
            text=data.get("text"),
            file_id=data.get("file_id"),
            replied_to_id=data.get("replied_to_id")
        )
    except Exception as e:
        error_message = str(e).replace("['", "").replace("']", "")
        await consumer.send(text_data=json.dumps({
            "type": "error",
            "error": str(_(error_message))
        }, ensure_ascii=False))