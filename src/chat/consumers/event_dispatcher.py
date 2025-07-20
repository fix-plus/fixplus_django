from .message_events import handle_send_message
from .status_events import handle_mark_delivered, handle_mark_read
from .event_schema import InputEvent
from typing import Any
import json

ACTION_HANDLERS = {
    "send_message": handle_send_message,
    "mark_delivered": handle_mark_delivered,
    "mark_read": handle_mark_read,
    "heartbeat": lambda consumer, _: consumer.send(text_data=json.dumps({
        "type": "heartbeat_response",
        "status": "ok"
    }, ensure_ascii=False))
}


async def dispatch_event(consumer: Any, data: InputEvent) -> None:
    """
    Dispatch incoming WebSocket events to the appropriate handler.
    Args:
        consumer: The WebSocket consumer instance.
        data: The event data.
    """
    action = data.get("action")
    if not action:
        await consumer.send(text_data=json.dumps({
            "type": "error",
            "error": "No action specified"
        }, ensure_ascii=False))
        return

    handler = ACTION_HANDLERS.get(action)
    if handler:
        await handler(consumer, data)
    else:
        await consumer.send(text_data=json.dumps({
            "type": "error",
            "error": f"Unknown action: {action}"
        }, ensure_ascii=False))