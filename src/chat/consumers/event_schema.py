from typing import TypedDict, Optional, Literal


# Input event schemas
class SendMessageEvent(TypedDict):
    action: Literal["send_message"]
    service_id: Optional[str]
    receiver_id: Optional[str]
    text: Optional[str]
    file_id: Optional[str]
    replied_to_id: Optional[str]


class MarkDeliveredEvent(TypedDict):
    action: Literal["mark_delivered"]
    message_id: str


class MarkReadEvent(TypedDict):
    action: Literal["mark_read"]
    message_id: str


class HeartbeatEvent(TypedDict):
    action: Literal["heartbeat"]


# Output event schemas
class NewMessagePayload(TypedDict):
    type: Literal["new_message"]
    service_id: str
    message: dict


class MessageStatusPayload(TypedDict):
    type: Literal["message_status"]
    service_id: str
    message_id: str
    status: Literal["delivered", "read"]


class ErrorPayload(TypedDict):
    type: Literal["error"]
    error: str


class HeartbeatResponsePayload(TypedDict):
    type: Literal["heartbeat_response"]
    status: Literal["ok"]


# All possible input events
InputEvent = SendMessageEvent | MarkDeliveredEvent | MarkReadEvent | HeartbeatEvent

# All possible output events
OutputEvent = NewMessagePayload | MessageStatusPayload | ErrorPayload | HeartbeatResponsePayload