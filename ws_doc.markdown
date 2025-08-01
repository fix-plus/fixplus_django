# Chat API and WebSocket Documentation

This document provides a comprehensive guide for using the Chat API and WebSocket integration for a real-time chat system. The APIs allow authenticated users to retrieve chat room lists and message histories, while the WebSocket enables real-time messaging, message status updates, and connection health checks via heartbeats.

## Table of Contents
- [Overview](#overview)
- [Authentication](#authentication)
- [REST API Endpoints](#rest-api-endpoints)
  - [Get Chat Room List](#get-chat-room-list)
  - [Get Chat Message History](#get-chat-message-history)
- [WebSocket Integration](#websocket-integration)
  - [Connecting to the WebSocket](#connecting-to-the-websocket)
  - [WebSocket Events](#websocket-events)
    - [Input Events](#input-events)
    - [Output Events](#output-events)
- [Error Handling](#error-handling)
- [Data Models](#data-models)
  - [Chat Room](#chat-room)
  - [Chat Message](#chat-message)
- [Usage Examples](#usage-examples)
  - [REST API Example](#rest-api-example)
  - [WebSocket Example](#websocket-example)

## Overview
The chat system is built using Django REST Framework (DRF) for REST APIs and Django Channels for WebSocket communication. It supports three types of chat rooms: `SERVICE`, `TECHNICIAN_DIRECT`, and `ADMIN_DIRECT`. The APIs provide access to chat rooms and message histories for authenticated users with verified mobile status. The WebSocket enables real-time messaging, including sending user and system messages, marking messages as delivered or read, and maintaining connection health.

## Authentication
All API endpoints and WebSocket connections require authentication. Users must be authenticated and have verified mobile status (enforced by `IsVerifiedMobileMixin`). The WebSocket uses the `scope["user"]` to verify authentication, and unauthenticated users will receive an error and be disconnected.

- **REST API**: Use standard HTTP authentication (e.g., Bearer token or session authentication).
- **WebSocket**: Authentication is handled via Django Channels middleware, passing the authenticated user in the `scope`.

## REST API Endpoints

### Get Chat Room List
- **Endpoint**: `GET /api/chat/rooms/`
- **Description**: Retrieves a paginated list of chat rooms the authenticated user is a member of.
- **Query Parameters**:
  - `room_type` (optional): Filter by room type (`SERVICE`, `TECHNICIAN_DIRECT`, `ADMIN_DIRECT`).
  - `search` (optional): Search term to filter rooms (max length: 200 characters).
  - `limit` (optional): Number of results per page (default: 100).
  - `offset` (optional): Starting point for pagination.
- **Response**: Paginated list of chat rooms.
  - **Status**: `200 OK`
  - **Body**: JSON object containing paginated results with chat room details.
  - **Example Response**:
    ```json
    {
      "count": 10,
      "next": "/api/chat/rooms/?limit=100&offset=100",
      "previous": null,
      "results": [
        {
          "room_id": "uuid",
          "type": "SERVICE",
          "unread_messages_count": 5,
          "last_message": {
            "message_id": "uuid",
            "text": "Hello!",
            "timestamp": "2025-07-31T15:35:00Z",
            "is_sent": true,
            "is_system_message": false,
            "sender": {
              "full_name": "John Doe",
              "avatar": "https://example.com/avatar.jpg",
              "role": "TECHNICIAN"
            }
          },
          "last_message_date": "2025-07-31T15:35:00Z",
          "counterpart": {
            "user_id": "uuid",
            "full_name": "Jane Smith",
            "avatar": "https://example.com/avatar2.jpg",
            "role": "ADMIN"
          },
          "service": {
            "id": "uuid",
            "created_at": "2025-07-31T10:00:00Z",
            "status": "ACTIVE"
          },
          "customer": {
            "full_name": "Customer Name",
            "phone_number": "+1234567890",
            "address": "123 Main St"
          }
        }
      ]
    }
    ```
- **Errors**:
  - `400 Bad Request`: Invalid query parameters.
  - `401 Unauthorized`: User is not authenticated or verified.

### Get Chat Message History
- **Endpoint**: `GET /api/chat/rooms/{room_id}/messages/`
- **Description**: Retrieves a paginated list of messages for a specific chat room. The user must be an active member of the room.
- **Path Parameters**:
  - `room_id`: UUID of the chat room.
- **Query Parameters**:
  - `limit` (optional): Number of messages per page (default: 100).
  - `offset` (optional): Starting point for pagination.
- **Response**: Paginated list of messages.
  - **Status**: `200 OK`
  - **Body**: JSON object containing paginated message history.
  - **Example Response**:
    ```json
    {
      "count": 50,
      "next": "/api/chat/rooms/{room_id}/messages/?limit=100&offset=100",
      "previous": null,
      "results": [
        {
          "id": "uuid",
          "is_sent": true,
          "text": "Hello, how can I help?",
          "file_id": null,
          "replied_from_id": null,
          "is_system_message": false,
          "timestamp": 1625247600,
          "sender_id": null,
          "sender_role": null,
          "sender_full_name": null,
          "sender_avatar": null,
          "is_delivered": true,
          "is_read": false,
          "room_id": "uuid"
        }
      ]
    }
    ```
- **Errors**:
  - `404 Not Found`: Room does not exist or user is not a member.
  - `401 Unauthorized`: User is not authenticated or verified.

## WebSocket Integration

### Connecting to the WebSocket
- **URL**: `wss://your-domain.com/ws/chat/`
- **Description**: Establishes a WebSocket connection for real-time chat functionality. Upon connection, the user is authenticated, their channel name is stored in Redis, and they are added to relevant groups (`user_<user_id>` and `room_<room_id>`). A heartbeat response confirms the connection.
- **Requirements**:
  - User must be authenticated (via Django Channels middleware).
  - User must have verified mobile status.
- **Connection Process**:
  1. Connect to the WebSocket endpoint.
  2. The server authenticates the user and stores the channel name in Redis.
  3. The user is added to their personal group and relevant chat room groups.
  4. A `heartbeat_response` is sent to confirm the connection.
- **Example Connection Response**:
  ```json
  {
    "type": "heartbeat_response",
    "status": "ok"
  }
  ```
- **Errors**:
  - `Authentication required`: If the user is not authenticated.
  - `Connection failed`: If group joining or Redis storage fails.

### WebSocket Events

#### Input Events
Clients send these events to the server to perform actions.

1. **Send Message**
   - **Action**: `send_message`
   - **Description**: Sends a new user message to a chat room (SERVICE, TECHNICIAN_DIRECT, or ADMIN_DIRECT).
   - **Payload**:
     ```json
     {
       "action": "send_message",
       "service_id": "uuid",
       "receiver_id": "uuid",
       "text": "Hello!",
       "file_id": "uuid",
       "replied_to_id": "uuid"
     }
     ```
   - **Notes**:
     - Either `service_id` (for SERVICE rooms) or `receiver_id` (for direct rooms) is required, but not both.
     - At least one of `text` or `file_id` must be provided.
     - `replied_to_id` is optional for replying to a previous message.
     - For direct rooms, the room type is determined based on whether the sender or receiver is a technician (`TECHNICIAN_DIRECT`) or not (`ADMIN_DIRECT`).

2. **Mark Delivered**
   - **Action**: `mark_delivered`
   - **Description**: Marks a message as delivered for the authenticated user.
   - **Payload**:
     ```json
     {
       "action": "mark_delivered",
       "message_id": "uuid"
     }
     ```
   - **Notes**:
     - The user must be a member of the room (for SERVICE rooms) to mark a message as delivered.

3. **Mark Read**
   - **Action**: `mark_read`
   - **Description**: Marks a message as read for the authenticated user.
   - **Payload**:
     ```json
     {
       "action": "mark_read",
       "message_id": "uuid"
     }
     ```
   - **Notes**:
     - The user must be a member of the room (for SERVICE rooms) to mark a message as read.

4. **Heartbeat**
   - **Action**: `heartbeat`
   - **Description**: Checks the connection status.
   - **Payload**:
     ```json
     {
       "action": "heartbeat"
     }
     ```

#### Output Events
The server sends these events to the client in response to actions or to notify of updates.

1. **New Message**
   - **Type**: `new_message`
   - **Description**: Notifies the client of a new message in a chat room (user or system message).
   - **Payload**:
     ```json
     {
       "type": "new_message",
       "room_id": "uuid",
       "service_id": "uuid",
       "message": {
         "id": "uuid",
         "room_id": "uuid",
         "is_sent": true,
         "text": "Hello!",
         "file_id": null,
         "replied_from_id": null,
         "is_system_message": false,
         "timestamp": 1625247600,
         "sender_id": "uuid",
         "sender_role": "TECHNICIAN",
         "sender_full_name": "John Doe",
         "sender_avatar": "https://example.com/avatar.jpg"
       }
     }
     ```
   - **Notes**:
     - `sender_id`, `sender_role`, `sender_full_name`, and `sender_avatar` are included only for non-system messages and messages not sent by the current user.
     - `service_id` is included for SERVICE rooms.

2. **Message Status**
   - **Type**: `message_status`
   - **Description**: Notifies the client of a message status update (delivered or read).
   - **Payload**:
     ```json
     {
       "type": "message_status",
       "service_id": "uuid",
       "message_id": "uuid",
       "status": "delivered"
     }
     ```
   - **Notes**:
     - `service_id` is included for SERVICE rooms.

3. **Heartbeat Response**
   - **Type**: `heartbeat_response`
   - **Description**: Confirms the WebSocket connection is active.
   - **Payload**:
     ```json
     {
       "type": "heartbeat_response",
       "status": "ok"
     }
     ```

4. **Error**
   - **Type**: `error`
   - **Description**: Indicates an error occurred during event processing.
   - **Payload**:
     ```json
     {
       "type": "error",
       "error": "Invalid JSON format"
     }
     ```

## Error Handling
Both REST APIs and WebSocket events handle errors consistently:
- **REST API**:
  - `400 Bad Request`: Invalid query parameters.
  - `401 Unauthorized`: Missing or invalid authentication.
  - `404 Not Found`: Resource (e.g., room or message) not found or user lacks access.
- **WebSocket**:
  - Errors are sent as JSON payloads with `type: "error"` and an `error` message.
  - Common errors include:
    - `No action specified`: Missing action in the input event.
    - `Unknown action`: Invalid action provided.
    - `Invalid JSON format`: Malformed JSON in the WebSocket message.
    - `Cannot provide both service_id and receiver_id`: Invalid input for `send_message`.
    - `Either service_id or receiver_id must be provided`: Missing required field.
    - `Either text or file_id must be provided`: Missing message content.
    - `Sender not found` or `Sender or receiver not found`: Invalid user IDs.
    - `Failed to get or create room`: Room creation or retrieval failed.
    - `Message not found`: Invalid message ID for status updates or replies.
    - `User not authorized to mark message as delivered/read`: User lacks permission for SERVICE rooms.
    - `Channel layer is not configured`: WebSocket server issue.

## Data Models

### Chat Room
- **Fields**:
  - `room_id`: UUID of the chat room.
  - `type`: Type of room (`SERVICE`, `TECHNICIAN_DIRECT`, `ADMIN_DIRECT`).
  - `unread_messages_count`: Number of unread messages for the user.
  - `last_message`: Details of the last message (see below).
  - `last_message_date`: Timestamp of the last message.
  - `counterpart`: Details of the other user in direct chats (`TECHNICIAN_DIRECT` or `ADMIN_DIRECT`).
  - `service`: Service details (for `SERVICE` rooms).
  - `customer`: Customer details (for `SERVICE` rooms).

### Chat Message
- **Fields**:
  - `id`: UUID of the message.
  - `is_sent`: Boolean indicating if the message was sent by the current user.
  - `text`: Message content (optional).
  - `file_id`: UUID of an attached file (optional).
  - `replied_from_id`: UUID of the message being replied to (optional).
  - `is_system_message`: Boolean indicating if the message is system-generated.
  - `timestamp`: Unix timestamp of the message.
  - `sender_id`: UUID of the sender (null for system messages or sent messages).
  - `sender_role`: Role of the sender (`TECHNICIAN`, `ADMIN`, `SUPER_ADMIN`, `UNKNOWN`).
  - `sender_full_name`: Full name of the sender.
  - `sender_avatar`: URL of the sender’s avatar.
  - `is_delivered`: Boolean indicating if the message was delivered.
  - `is_read`: Boolean indicating if the message was read.

## Usage Examples

### REST API Example
**Request**: Get chat rooms with a search term.
```bash
curl -H "Authorization: Bearer <token>" \
     "https://your-domain.com/api/chat/rooms/?search=support&limit=10"
```

**Response**:
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "room_id": "123e4567-e89b-12d3-a456-426614174000",
      "type": "SERVICE",
      "unread_messages_count": 3,
      "last_message": {
        "message_id": "789e0123-e89b-12d3-a456-426614174001",
        "text": "Need assistance?",
        "timestamp": "2025-07-31T15:35:00Z",
        "is_sent": false,
        "is_system_message": false,
        "sender": {
          "full_name": "Support Team",
          "avatar": "https://example.com/support.jpg",
          "role": "ADMIN"
        }
      },
      "last_message_date": "2025-07-31T15:35:00Z",
      "counterpart": null,
      "service": {
        "id": "456e7890-e89b-12d3-a456-426614174002",
        "created_at": "2025-07-31T10:00:00Z",
        "status": "ACTIVE"
      },
      "customer": {
        "full_name": "Customer Name",
        "phone_number": "+1234567890",
        "address": "123 Main St"
      }
    }
  ]
}
```

### WebSocket Example
**JavaScript Client**:
```javascript
const socket = new WebSocket('wss://your-domain.com/ws/chat/');

socket.onopen = () => {
  console.log('Connected to WebSocket');
  // Send heartbeat
  socket.send(JSON.stringify({ action: 'heartbeat' }));
};

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);

  if (data.type === 'new_message') {
    console.log('New message:', data.message.text, 'in room:', data.room_id);
  } else if (data.type === 'message_status') {
    console.log(`Message ${data.message_id} is ${data.status}`);
  } else if (data.type === 'error') {
    console.error('Error:', data.error);
  }
};

socket.onerror = (error) => {
  console.error('WebSocket error:', error);
};

socket.onclose = () => {
  console.log('WebSocket closed');
};

// Send a message to a service room
socket.send(JSON.stringify({
  action: 'send_message',
  service_id: '456e7890-e89b-12d3-a456-426614174002',
  text: 'Hello, I need help!'
}));

// Send a message to a direct room
socket.send(JSON.stringify({
  action: 'send_message',
  receiver_id: '789e0123-e89b-12d3-a456-426614174003',
  text: 'Hi, are you available?',
  file_id: '123e4567-e89b-12d3-a456-426614174004'
}));

// Mark a message as read
socket.send(JSON.stringify({
  action: 'mark_read',
  message_id: '789e0123-e89b-12d3-a456-426614174001'
}));
```

**Expected Output**:
- On connection:
  ```json
  { "type": "heartbeat_response", "status": "ok" }
  ```
- On new message:
  ```json
  {
    "type": "new_message",
    "room_id": "123e4567-e89b-12d3-a456-426614174000",
    "service_id": "456e7890-e89b-12d3-a456-426614174002",
    "message": {
      "id": "789e0123-e89b-12d3-a456-426614174005",
      "is_sent": true,
      "text": "Hello, I need help!",
      "file_id": null,
      "replied_from_id": null,
      "is_system_message": false,
      "timestamp": 1625247600
    }
  }
  ```
- On message status update:
  ```json
  {
    "type": "message_status",
    "service_id": "456e7890-e89b-12d3-a456-426614174002",
    "message_id": "789e0123-e89b-12d3-a456-426614174001",
    "status": "read"
  }
  ```