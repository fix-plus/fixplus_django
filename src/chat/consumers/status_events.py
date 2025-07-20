from channels.db import database_sync_to_async
from src.chat.services.message import mark_message_delivered, mark_message_read
from src.chat.consumers.event_schema import MarkDeliveredEvent, MarkReadEvent
from typing import Any


async def handle_mark_delivered(consumer: Any, data: MarkDeliveredEvent) -> None:
    """
    Handle the mark_delivered event.
    Args:
        consumer: The WebSocket consumer instance.
        data: The event data containing message_id.
    """
    try:
        await database_sync_to_async(mark_message_delivered)(
            message_id=data["message_id"],
            receiver_id=str(consumer.user.id)
        )
    except Exception as e:
        await consumer.send(text_data=json.dumps({
            "type": "error",
            "error": str(e)
        }, ensure_ascii=False))


async def handle_mark_read(consumer: Any, data: MarkReadEvent) -> None:
    """
    Handle the mark_read event.
    Args:
        consumer: The WebSocket consumer instance.
        data: The event data containing message_id.
    """
    try:
        await database_sync_to_async(mark_message_read)(
            message_id=data["message_id"],
            user_id=str(consumer.user.id)
        )
    except Exception as e:
        await consumer.send(text_data=json.dumps({
            "type": "error",
            "error": str(e)
        }, ensure_ascii=False))