# WebSocket Chat System Technical Documentation

This document provides a concise, technical overview of the WebSocket chat system's input and output events, including JSON examples, mandatory/optional fields, and sample errors.

## Input Events

Defined in `event_schema.py`, these are client-sent events.

1. **SendMessageEvent**
   - **Action**: `send_message`
   - **Fields**:
     - `action`: `"send_message"` (mandatory, Literal)
     - `room_id`: Room ID (optional, str)
     - `service_id`: Service ID (optional, str)
     - `receiver_id`: Receiver user ID (optional, str)
     - `text`: Message text (optional, str)
     - `file_id`: File ID (optional, str)
     - `replied_to_id`: Replied-to message ID (optional, str)
   - **Description**: Sends a message to a room or creates a direct room.
   - **Input JSON Example**:
     ```json
     {
       "action": "send_message",
       "room_id": "123",
       "service_id": "456",
       "receiver_id": "789",
       "text": "Hello, how are you?",
       "file_id": null,
       "replied_to_id": null
     }
     ```
   - **Output JSON Example** (Success):
     ```json
     {
       "type": "new_message",
       "data": {
         "room_id": "123",
         "service_id": "456",
         "message": {
           "id": "msg_001",
           "is_sent": true,
           "text": "Hello, how are you?",
           "file_id": null,
           "replied_from_id": null,
           "is_system_message": false,
           "timestamp": 1697059200,
           "sender": null
         }
       }
     }
     ```
   - **Error Example**:
     ```json
     {
       "type": "error",
       "error": "Room not found"
     }
     ```

2. **MarkDeliveredEvent**
   - **Action**: `mark_delivered`
   - **Fields**:
     - `action`: `"mark_delivered"` (mandatory, Literal)
     - `message_id`: Message ID (mandatory, str)
   - **Description**: Marks a message as delivered.
   - **Input JSON Example**:
     ```json
     {
       "action": "mark_delivered",
       "message_id": "msg_001"
     }
     ```
   - **Output JSON Example** (Success):
     ```json
     {
       "type": "message_status",
       "data": {
         "service_id": "456",
         "message_id": "msg_001",
         "status": "delivered"
       }
     }
     ```
   - **Error Example**:
     ```json
     {
       "type": "error",
       "error": "Message or room not found"
     }
     ```

3. **MarkReadEvent**
   - **Action**: `mark_read`
   - **Fields**:
     - `action`: `"mark_read"` (mandatory, Literal)
     - `message_id`: Message ID (mandatory, str)
   - **Description**: Marks a message as read.
   - **Input JSON Example**:
     ```json
     {
       "action": "mark_read",
       "message_id": "msg_001"
     }
     ```
   - **Output JSON Example** (Success):
     ```json
     {
       "type": "message_status",
       "data": {
         "service_id": "456",
         "message_id": "msg_001",
         "status": "read"
       }
     }
     ```
   - **Error Example**:
     ```json
     {
       "type": "error",
       "error": "Message or room not found"
     }
     ```

4. **HeartbeatEvent**
   - **Action**: `heartbeat`
   - **Fields**:
     - `action`: `"heartbeat"` (mandatory, Literal)
   - **Description**: Checks server connectivity.
   - **Input JSON Example**:
     ```json
     {
       "action": "heartbeat"
     }
     ```
   - **Output JSON Example** (Success):
     ```json
     {
       "type": "heartbeat_response",
       "status": "ok"
     }
     ```
   - **Error Example**:
     ```json
     {
       "type": "error",
       "error": "Invalid JSON format"
     }
     ```

5. **NewRoomEvent**
   - **Action**: `new_room`
   - **Fields**:
     - `action`: `"new_room"` (mandatory, Literal)
     - `room_id`: Room ID (mandatory, str)
   - **Description**: Notifies of a new direct room.
   - **Input JSON Example**:
     ```json
     {
       "action": "new_room",
       "room_id": "123"
     }
     ```
   - **Output JSON Example** (Success):
     ```json
     {
       "type": "new_room",
       "data": {
         "room_id": "123",
         "type": "TECHNICIAN_DIRECT",
         "unread_messages_count": 0,
         "last_message": null,
         "counterpart": {
           "user_id": "789",
           "full_name": "John Doe",
           "avatar": "https://example.com/avatar.jpg",
           "role": "TECHNICIAN"
         },
         "service": null,
         "customer": null
       }
     }
     ```
   - **Error Example**:
     ```json
     {
       "type": "error",
       "error": "Room is not a direct room"
     }
     ```

## Output Events

Defined in `event_schema.py`, these are server-sent events.

1. **NewRoomPayload**
   - **Type**: `new_room`
   - **Fields**:
     - `type`: `"new_room"` (mandatory, Literal)
     - `data`:
       - `room_id`: Room ID (mandatory, str)
       - `type`: Room type (mandatory, str)
       - `unread_messages_count`: Unread count (mandatory, int)
       - `last_message`: Last message (optional, LastMessagePayload)
       - `counterpart`: Counterpart user (optional, CounterpartPayload)
       - `service`: Service details (optional, ServicePayload)
       - `customer`: Customer details (optional, CustomerPayload)
   - **Description**: Sent for new or joined rooms.

2. **NewMessagePayload**
   - **Type**: `new_message`
   - **Fields**:
     - `type`: `"new_message"` (mandatory, Literal)
     - `data`:
       - `room_id`: Room ID (mandatory, str)
       - `service_id`: Service ID (optional, str)
       - `message`:
         - `id`: Message ID (mandatory, str)
         - `is_sent`: Sent by user (mandatory, bool)
         - `text`: Message text (optional, str)
         - `file_id`: File ID (optional, str)
         - `replied_from_id`: Replied-to ID (optional, str)
         - `is_system_message`: System message flag (mandatory, bool)
         - `timestamp`: Timestamp (mandatory, int)
         - `sender`: Sender details (optional, SenderPayload)
   - **Description**: Sent for new messages.

3. **MessageStatusPayload**
   - **Type**: `message_status`
   - **Fields**:
     - `type`: `"message_status"` (mandatory, Literal)
     - `data`:
       - `service_id`: Service ID (optional, str)
       - `message_id`: Message ID (mandatory, str)
       - `status`: Status (delivered/read) (mandatory, str)
   - **Description**: Sent for message status updates.

4. **HeartbeatResponsePayload**
   - **Type**: `heartbeat_response`
   - **Fields**:
     - `type`: `"heartbeat_response"` (mandatory, Literal)
     - `data`:
       - `status`: Status (mandatory, str, usually "ok")
   - **Description**: Confirms server connectivity.

5. **UpdateUnreadMessageCountPayload**
   - **Type**: `unread_message_count`
   - **Fields**:
     - `type`: `"unread_message_count"` (mandatory, Literal)
     - `data`:
       - `room_id`: Room ID (mandatory, str)
       - `unread_count`: Unread message count (mandatory, int)
   - **Description**: Sent for unread message count updates.

6. **ErrorPayload**
   - **Type**: `error`
   - **Fields**:
     - `type`: `"error"` (mandatory, Literal)
     - `error` or `data.error`: Error message (mandatory, str)
   - **Description**: Sent for errors.

## Common Payloads

- **SenderPayload**:
  - `id`: User ID (optional, str)
  - `full_name`: Full name (optional, str)
  - `avatar`: Avatar URL (optional, str)
  - `role`: Role (TECHNICIAN/ADMIN/SUPER_ADMIN/UNKNOWN) (optional, str)
- **LastMessagePayload**:
  - `message_id`: Message ID (mandatory, str)
  - `text`: Message text (optional, str)
  - `timestamp`: ISO timestamp (mandatory, str)
  - `is_sent`: Sent by user (mandatory, bool)
  - `is_system_message`: System message flag (mandatory, bool)
  - `sender`: Sender details (optional, SenderPayload)
  - `file_id`: File ID (optional, str)
  - `replied_from_id`: Replied-to ID (optional, str)
- **CounterpartPayload**:
  - `user_id`: User ID (mandatory, str)
  - `full_name`: Full name (optional, str)
  - `avatar`: Avatar URL (optional, str)
  - `role`: Role (mandatory, str)
- **ServicePayload**:
  - `id`: Service ID (mandatory, str)
  - `created_at`: ISO timestamp (mandatory, str)
  - `status`: Service status (mandatory, str)
- **CustomerPayload**:
  - `full_name`: Full name (optional, str)
  - `phone_number`: Phone number (optional, str)
  - `address`: Address (optional, str)

## Error Handling

- **Common Errors**:
  - Invalid JSON: `{"type": "error", "error": "Invalid JSON format"}`
  - Missing action: `{"type": "error", "error": "No action specified"}`
  - Unknown action: `{"type": "error", "error": "Unknown action: <action>"}`
  - Authentication: `{"type": "error", "error": "Authentication required"}`
  - Room not found: `{"type": "error", "error": "Room not found"}`
  - Channel layer not configured: `{"type": "error", "error": "Channel layer is not configured"}`