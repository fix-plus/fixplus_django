# WebSocket API Documentation

This document provides detailed information on how to interact with the WebSocket service for the chat application. The WebSocket API enables real-time communication, allowing clients to send user messages, mark messages as delivered or read, and maintain connection health through heartbeats. System messages are sent server-side only and are not accessible to clients.

## WebSocket Endpoint

- **URL**: `ws://localhost:8000/ws/chat/?token=<jwt_token>`
- **Protocol**: WebSocket (ws)
- **Authentication**: The WebSocket connection requires an authenticated user. Authentication is handled via a JWT token passed as a query parameter (`token`). The token must be valid, non-expired, and signed with the server's `SECRET_KEY`.
- **Connection Notes**:
  - Clients must send a `heartbeat` event every 30 seconds to keep the connection alive.
  - The server responds to heartbeats with a `heartbeat_response` event.
  - Unauthorized connections (e.g., invalid or expired token) are rejected with an `error` event and closed immediately.

## Event Schemas

The WebSocket API uses JSON-formatted events for communication. Below are the input and output event schemas.

### Input Events
Clients can send the following events to the server:

1. **send_message**
   - **Description**: Sends a new user message to a chat room (SERVICE or direct).
   - **Schema**:
     ```json
     {
       "action": "send_message",
       "service_id": "<string|null>",
       "receiver_id": "<string|null>",
       "text": "<string|null>",
       "file_id": "<string|null>",
       "replied_to_id": "<string|null>"
     }
     ```
   - **Fields**:
     - `action`: Must be `"send_message"`.
     - `service_id`: Required for SERVICE rooms, must be null for direct rooms.
     - `receiver_id`: Required for direct rooms (TECHNICIAN_DIRECT or ADMIN_DIRECT), must be null for SERVICE rooms.
     - `text`: Message text (optional if file_id is provided).
     - `file_id`: ID of an attached file (optional).
     - `replied_to_id`: ID of the message being replied to (optional).
   - **Room Type Logic**:
     - If `service_id` is non-null, the room type is `SERVICE`.
     - If `receiver_id` is non-null (and `service_id` is null):
       - If the sender or receiver is in the `TECHNICIAN` group, the room type is `TECHNICIAN_DIRECT`.
       - Otherwise, the room type is `ADMIN_DIRECT`.

2. **mark_delivered**
   - **Description**: Marks a message as delivered.
   - **Schema**:
     ```json
     {
       "action": "mark_delivered",
       "message_id": "<string>"
     }
     ```
   - **Fields**:
     - `action`: Must be `"mark_delivered"`.
     - `message_id`: ID of the message to mark as delivered.

3. **mark_read**
   - **Description**: Marks a message as read.
   - **Schema**:
     ```json
     {
       "action": "mark_read",
       "message_id": "<string>"
     }
     ```
   - **Fields**:
     - `action`: Must be `"mark_read"`.
     - `message_id`: ID of the message to mark as read.

4. **heartbeat**
   - **Description**: Sent by the client to keep the WebSocket connection alive.
   - **Schema**:
     ```json
     {
       "action": "heartbeat"
     }
     ```
   - **Fields**:
     - `action`: Must be `"heartbeat"`.

### Output Events
The server sends the following events to clients:

1. **new_message**
   - **Description**: Notifies clients of a new message (user or system) in a room.
   - **Schema**:
     ```json
     {
       "type": "new_message",
       "service_id": "<string|null>",
       "message": {
         "id": "<string>",
         "sender": "<string|null>",
         "text": "<string|null>",
         "file_id": "<string|null>",
         "replied_from_id": "<string|null>",
         "is_delivered": <boolean>,
         "is_read": <boolean>,
         "is_system_message": <boolean>,
         "timestamp": <integer>,
         "is_sent": <boolean>
       }
     }
     ```
   - **Fields**:
     - `type`: Always `"new_message"`.
     - `service_id`: ID of the service (null for direct rooms).
     - `message`: Details of the new message.
       - `id`: Message ID.
       - `sender`: ID of the sender (null for system messages).
       - `text`: Message text (null if file-only).
       - `file_id`: ID of the attached file (null if none).
       - `replied_from_id`: ID of the replied-to message (null if none).
       - `is_delivered`: Whether the message is delivered.
       - `is_read`: Whether the message is read.
       - `is_system_message`: True for system messages, false for user messages.
       - `timestamp`: Unix timestamp of message creation.
       - `is_sent`: True if the message was sent by the receiving user.

2. **message_status**
   - **Description**: Notifies clients of a message status update (delivered or read).
   - **Schema**:
     ```json
     {
       "type": "message_status",
       "service_id": "<string|null>",
       "message_id": "<string>",
       "status": "<string>"
     }
     ```
   - **Fields**:
     - `type`: Always `"message_status"`.
     - `service_id`: ID of the service (null for direct rooms).
     - `message_id`: ID of the message.
     - `status`: Either `"delivered"` or `"read"`.

3. **error**
   - **Description**: Sent when an error occurs (e.g., invalid input, unauthorized action, authentication failure).
   - **Schema**:
     ```json
     {
       "type": "error",
       "error": "<string>"
     }
     ```
   - **Fields**:
     - `type`: Always `"error"`.
     - `error`: Translated error message (using Django's `gettext_lazy`).

4. **heartbeat_response**
   - **Description**: Response to a heartbeat event to confirm the connection is alive.
   - **Schema**:
     ```json
     {
       "type": "heartbeat_response",
       "status": "ok"
     }
     ```
   - **Fields**:
     - `type`: Always `"heartbeat_response"`.
     - `status`: Always `"ok"`.

## System Messages
System messages are sent server-side only and are restricted to SERVICE rooms. Clients cannot send system messages. To send a system message, use the server-side `send_system_message` function with the following parameters:
- `service_id`: Required.
- `text`: Optional message text.
- `file_id`: Optional file ID.
- `replied_to_id`: Optional ID of the message being replied to.

Example server-side call (Python):
```python
from src.chat.services.message import send_system_message

send_system_message(
    service_id="123e4567-e89b-12d3-a456-426614174000",
    text="System alert: Maintenance scheduled at 10 PM."
)
```

## Testing with Postman

Postman supports WebSocket testing (since version 8.0). Follow these steps to test the WebSocket API:

1. **Open Postman**:
   - Create a new WebSocket request by selecting "New" > "WebSocket".

2. **Configure the WebSocket URL**:
   - Set the URL to `ws://localhost:8000/ws/chat/?token=<jwt_token>`.
   - Replace `<jwt_token>` with a valid JWT token.

3. **Connect to the WebSocket**:
   - Click "Connect" to establish the WebSocket connection.
   - Upon successful connection, the server sends a `heartbeat_response`:
     ```json
     {
       "type": "heartbeat_response",
       "status": "ok"
     }
     ```
   - If the token is invalid or expired, expect an `error` event:
     ```json
     {
       "type": "error",
       "error": "Invalid token"
     }
     ```

4. **Send Events**:
   - Use the Postman message input to send JSON-formatted events (`send_message`, `mark_delivered`, etc.).
   - Ensure the JSON matches the input event schemas above.

5. **Monitor Responses**:
   - Postman displays incoming messages in the message log.
   - Check for `new_message`, `message_status`, `error`, or `heartbeat_response` events.

## Example Requests and Responses

### 1. Connect with Valid Token
- **URL**: `ws://localhost:8000/ws/chat/?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- **Successful Response**:
  ```json
  {
    "type": "heartbeat_response",
    "status": "ok"
  }
  ```

### 2. Connect with Invalid Token
- **URL**: `ws://localhost:8000/ws/chat/?token=invalid_token`
- **Response**:
  ```json
  {
    "type": "error",
    "error": "Invalid token"
  }
  ```

### 3. Connect with Expired Token
- **URL**: `ws://localhost:8000/ws/chat/?token=expired_token`
- **Response**:
  ```json
  {
    "type": "error",
    "error": "Token has expired"
  }
  ```

### 4. Connect with No Token
- **URL**: `ws://localhost:8000/ws/chat/`
- **Response**:
  ```json
  {
    "type": "error",
    "error": "No token provided"
  }
  ```

### 5. Send Message (SERVICE Room)
- **Request**:
  ```json
  {
    "action": "send_message",
    "service_id": "123e4567-e89b-12d3-a456-426614174000",
    "receiver_id": null,
    "text": "Hello, this is a test message!",
    "file_id": null,
    "replied_to_id": null
  }
  ```
- **Successful Response** (sent to all room participants):
  ```json
  {
    "type": "new_message",
    "service_id": "123e4567-e89b-12d3-a456-426614174000",
    "message": {
      "id": "789e1234-f56b-78d9-a123-426614174001",
      "sender": "user_1",
      "text": "Hello, this is a test message!",
      "file_id": null,
      "replied_from_id": null,
      "is_delivered": false,
      "is_read": false,
      "is_system_message": false,
      "timestamp": 1737027612,
      "is_sent": true
    }
  }
  ```
- **Failed Response** (e.g., invalid service_id):
  ```json
  {
    "type": "error",
    "error": "Failed to get or create room: Service not found"
  }
  ```

### 6. Send Message (Direct Room)
- **Request** (TECHNICIAN_DIRECT, if sender or receiver is TECHNICIAN):
  ```json
  {
    "action": "send_message",
    "service_id": null,
    "receiver_id": "user_2",
    "text": "Hi, can you check this issue?",
    "file_id": null,
    "replied_to_id": null
  }
  ```
- **Successful Response** (sent to both sender and receiver):
  ```json
  {
    "type": "new_message",
    "service_id": null,
    "message": {
      "id": "789e1234-f56b-78d9-a123-426614174002",
      "sender": "user_1",
      "text": "Hi, can you check this issue?",
      "file_id": null,
      "replied_from_id": null,
      "is_delivered": false,
      "is_read": false,
      "is_system_message": false,
      "timestamp": 1737027613,
      "is_sent": true
    }
  }
  ```
- **Failed Response** (e.g., receiver not found):
  ```json
  {
    "type": "error",
    "error": "Sender or receiver not found"
  }
  ```

### 7. Mark Message as Delivered
- **Request**:
  ```json
  {
    "action": "mark_delivered",
    "message_id": "789e1234-f56b-78d9-a123-426614174001"
  }
  ```
- **Successful Response** (sent to all room participants):
  ```json
  {
    "type": "message_status",
    "service_id": "123e4567-e89b-12d3-a456-426614174000",
    "message_id": "789e1234-f56b-78d9-a123-426614174001",
    "status": "delivered"
  }
  ```
- **Failed Response** (e.g., unauthorized user):
  ```json
  {
    "type": "error",
    "error": "User not authorized to mark message as delivered"
  }
  ```

### 8. Mark Message as Read
- **Request**:
  ```json
  {
    "action": "mark_read",
    "message_id": "789e1234-f56b-78d9-a123-426614174001"
  }
  ```
- **Successful Response** (sent to all room participants):
  ```json
  {
    "type": "message_status",
    "service_id": "123e4567-e89b-12d3-a456-426614174000",
    "message_id": "789e1234-f56b-78d9-a123-426614174001",
    "status": "read"
  }
  ```
- **Failed Response** (e.g., message not found):
  ```json
  {
    "type": "error",
    "error": "Message not found"
  }
  ```

### 9. Heartbeat
- **Request**:
  ```json
  {
    "action": "heartbeat"
  }
  ```
- **Successful Response**:
  ```json
  {
    "type": "heartbeat_response",
    "status": "ok"
  }
  ```
- **Failed Response**: None (if the server doesn't respond, the client should attempt to reconnect).

## Client-Side Example (JavaScript)

Below is a sample JavaScript client to interact with the WebSocket API:

<xaiArtifact artifact_id="a29c1ae9-2a2b-4ddd-bacd-d217581a1265" artifact_version_id="66c3f0cb-7817-4499-8ea2-7fa582c26a3c" title="client.js" contentType="text/javascript">
// Sample WebSocket client implementation
const ws = new WebSocket('ws://localhost:8000/ws/chat/?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...');

ws.onopen = () => {
    console.log('Connected to WebSocket');
    // Start heartbeat every 30 seconds
    setInterval(() => {
        ws.send(JSON.stringify({ action: 'heartbeat' }));
    }, 30000);
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    switch (data.type) {
        case 'new_message':
            console.log('New message:', data.message);
            // Update UI with new message (handle system messages differently if is_system_message is true)
            break;
        case 'message_status':
            console.log('Message status:', data.status, 'for message', data.message_id);
            // Update message status in UI
            break;
        case 'error':
            console.error('Error:', data.error);
            // Show translated error to user
            break;
        case 'heartbeat_response':
            console.log('Heartbeat response:', data.status);
            break;
        default:
            console.warn('Unknown event type:', data.type);
    }
};

ws.onclose = () => {
    console.log('WebSocket disconnected. Reconnecting...');
    // Implement reconnection logic
};

// Example: Send a message (SERVICE room)
function sendServiceMessage(serviceId, text, fileId, repliedToId) {
    ws.send(JSON.stringify({
        action: 'send_message',
        service_id: serviceId,
        receiver_id: null,
        text: text,
        file_id: fileId,
        replied_to_id: repliedToId
    }));
}

// Example: Send a direct message
function sendDirectMessage(receiverId, text, fileId, repliedToId) {
    ws.send(JSON.stringify({
        action: 'send_message',
        service_id: null,
        receiver_id: receiverId,
        text: text,
        file_id: fileId,
        replied_to_id: repliedToId
    }));
}

// Example: Mark message as delivered
function markDelivered(messageId) {
    ws.send(JSON.stringify({
        action: 'mark_delivered',
        message_id: messageId
    }));
}

// Example: Mark message as read
function markRead(messageId) {
    ws.send(JSON.stringify({
        action: 'mark_read',
        message_id: messageId
    }));
}