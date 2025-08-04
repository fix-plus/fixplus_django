from typing import TypedDict, Optional, Literal

# Input event schemas
class SendMessageEvent(TypedDict):
    action: Literal["send_message"]
    room_id: Optional[str]
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

class NewRoomEvent(TypedDict):
    action: Literal["new_room"]
    room_id: str

# Output event schemas
class SenderPayload(TypedDict):
    full_name: str
    avatar: Optional[str]
    role: str

class LastMessagePayload(TypedDict):
    message_id: str
    text: Optional[str]
    timestamp: str
    is_sent: bool
    is_system_message: bool
    sender: Optional[SenderPayload]

class CounterpartPayload(TypedDict):
    user_id: str
    full_name: str
    avatar: Optional[str]
    role: str

class NewRoomPayload(TypedDict):
    type: Literal["new_room"]
    room_id: str
    type: str
    unread_messages_count: int
    last_message: Optional[LastMessagePayload]
    counterpart: Optional[CounterpartPayload]
    service: Optional[dict]
    customer: Optional[dict]

class NewMessagePayload(TypedDict):
    type: Literal["new_message"]
    room_id: str
    service_id: Optional[str]
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

class UpdateUnreadMessageCountPayload(TypedDict):
    type: Literal["unread_message_count"]
    room_id: str
    unread_count: int

# All possible input events
InputEvent = SendMessageEvent | MarkDeliveredEvent | MarkReadEvent | HeartbeatEvent | NewRoomEvent

# All possible output events
OutputEvent = NewRoomPayload | NewMessagePayload | MessageStatusPayload | ErrorPayload | HeartbeatResponsePayload | UpdateUnreadMessageCountPayload