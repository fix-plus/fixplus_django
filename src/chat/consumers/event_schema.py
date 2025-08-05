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

# Common payload schemas
class SenderPayload(TypedDict):
    id: Optional[str]
    full_name: Optional[str]
    avatar: Optional[str]
    role: Optional[str]

class LastMessagePayload(TypedDict):
    message_id: str
    text: Optional[str]
    timestamp: str
    is_sent: bool
    is_system_message: bool
    sender: Optional[SenderPayload]
    file_id: Optional[str]
    replied_from_id: Optional[str]

class CounterpartPayload(TypedDict):
    user_id: str
    full_name: Optional[str]
    avatar: Optional[str]
    role: str

class ServicePayload(TypedDict):
    id: str
    created_at: str
    status: str

class CustomerPayload(TypedDict):
    full_name: Optional[str]
    phone_number: Optional[str]
    address: Optional[str]

# Output event schemas
class NewRoomPayload(TypedDict):
    type: Literal["new_room"]
    data: dict  # Will contain room_id, type, unread_messages_count, last_message, counterpart, service, customer

class NewMessagePayload(TypedDict):
    type: Literal["new_message"]
    data: dict  # Will contain room_id, service_id, message

class MessageStatusPayload(TypedDict):
    type: Literal["message_status"]
    data: dict  # Will contain service_id, message_id, status

class ErrorPayload(TypedDict):
    type: Literal["error"]
    data: dict  # Will contain error message

class HeartbeatResponsePayload(TypedDict):
    type: Literal["heartbeat_response"]
    data: dict  # Will contain status

class UpdateUnreadMessageCountPayload(TypedDict):
    type: Literal["unread_message_count"]
    data: dict  # Will contain room_id, unread_count

# All possible input events
InputEvent = SendMessageEvent | MarkDeliveredEvent | MarkReadEvent | HeartbeatEvent | NewRoomEvent

# All possible output events
OutputEvent = NewRoomPayload | NewMessagePayload | MessageStatusPayload | ErrorPayload | HeartbeatResponsePayload | UpdateUnreadMessageCountPayload