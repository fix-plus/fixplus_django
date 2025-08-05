import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .group_manager import join_user_groups, leave_user_groups
from .event_dispatcher import dispatch_event
from .event_schema import InputEvent, OutputEvent
from ..services.channel_storage import channel_storage
import logging
import traceback

logger = logging.getLogger(__name__)

class ChatWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Handle WebSocket connection.
        Authenticate user and join relevant groups.
        """
        self.user = self.scope["user"]

        # Extract base_url from scope headers
        base_url = None
        for header_name, header_value in self.scope['headers']:
            if header_name.decode('utf-8').lower() == 'host':
                # Assume HTTPS for production, fallback to HTTP if explicitly set
                protocol = 'https' if self.scope.get('scheme', 'http') == 'https' else 'http'
                base_url = f"{protocol}://{header_value.decode('utf-8')}"
                break
        self.scope['base_url'] = base_url or 'http://localhost:8000'  # Fallback for local development

        # Accept the connection first
        await self.accept()

        # Check for authentication errors from middleware
        if 'error' in self.scope:
            await self.send(text_data=json.dumps({
                "type": "error",
                "error": self.scope['error']
            }, ensure_ascii=False))
            await self.close()
            return

        # Check if user is authenticated
        if not self.user.is_authenticated:
            await self.send(text_data=json.dumps({
                "type": "error",
                "error": "Authentication required"
            }, ensure_ascii=False))
            await self.close()
            return

        try:
            # Store channel name in Redis
            channel_storage.store_channel_name(str(self.user.id), self.channel_name)

            # Join user groups
            await join_user_groups(self)

            # Send initial heartbeat response
            await self.send(text_data=json.dumps({
                "type": "heartbeat_response",
                "status": "ok"
            }, ensure_ascii=False))
        except Exception as e:
            logger.error(f"Connection failed for user {self.user.id}: {str(e)}\n{traceback.format_exc()}")
            await self.send(text_data=json.dumps({
                "type": "error",
                "error": f"Connection failed: {str(e)}"
            }, ensure_ascii=False))
            await self.close()

    async def disconnect(self, close_code):
        """
        Handle WebSocket disconnection.
        Remove consumer from all groups.
        """
        try:
            # Remove channel name from Redis
            channel_storage.remove_channel_name(str(self.user.id))

            # Leave all user groups
            await leave_user_groups(self)
        except Exception as e:
            logger.error(f"Error during disconnect for user {self.user.id}: {str(e)}")

    async def receive(self, text_data: str):
        """
        Handle incoming WebSocket messages.
        Args:
            text_data: Raw JSON string received from the client.
        """
        try:
            data: InputEvent = json.loads(text_data)
            await dispatch_event(self, data)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON format received: {text_data}")
            await self.send(text_data=json.dumps({
                "type": "error",
                "error": "Invalid JSON format"
            }, ensure_ascii=False))
        except ValidationError as e:
            error_message = str(e).replace("['", "").replace("']", "")
            logger.error(f"Validation error: {error_message}")
            await self.send(text_data=json.dumps({
                "type": "error",
                "error": error_message
            }, ensure_ascii=False))
        except Exception as e:
            logger.error(f"Unexpected error in receive: {str(e)}\n{traceback.format_exc()}")
            await self.send(text_data=json.dumps({
                "type": "error",
                "error": f"An unexpected error occurred: {str(e)}"
            }, ensure_ascii=False))

    async def chat_message(self, event: dict):
        """
        Handle chat_message event.
        Send new message payload to the client.
        Args:
            event: Event data containing message_id.
        """
        from .utils import format_message_payload
        try:
            payload = await format_message_payload(
                event["message_id"],
                self.user.id,
                base_url=self.scope.get('base_url')
            )
            await self.send(text_data=json.dumps(payload, ensure_ascii=False))
        except Exception as e:
            logger.error(
                f"Failed to process chat_message for message {event['message_id']}: {str(e)}\n{traceback.format_exc()}")
            await self.send(text_data=json.dumps({
                "type": "error",
                "data": {"error": f"Failed to process message: {str(e)}"}
            }, ensure_ascii=False))

    async def message_status(self, event: dict):
        """
        Handle message_status event.
        Send status update payload to the client.
        Args:
            event: Event data containing message_id and status.
        """
        from .utils import format_status_payload
        try:
            payload = await format_status_payload(event["message_id"], event["status"])
            await self.send(text_data=json.dumps(payload, ensure_ascii=False))
        except Exception as e:
            logger.error(
                f"Failed to process message_status for message {event['message_id']}: {str(e)}\n{traceback.format_exc()}")
            await self.send(text_data=json.dumps({
                "type": "error",
                "data": {"error": f"Failed to process status: {str(e)}"}
            }, ensure_ascii=False))

    async def unread_message_count(self, event: dict):
        """
        Handle unread_message_count event.
        Send unread message count for a specific room to the client.
        Args:
            event: Event data containing room_id.
        """
        from .utils import format_unread_count_payload
        try:
            payload = await format_unread_count_payload(event["room_id"], self.user.id)
            await self.send(text_data=json.dumps(payload, ensure_ascii=False))
        except Exception as e:
            logger.error(
                f"Failed to process unread_message_count for room {event['room_id']}: {str(e)}\n{traceback.format_exc()}")
            await self.send(text_data=json.dumps({
                "type": "error",
                "data": {"error": f"Failed to process unread count: {str(e)}"}
            }, ensure_ascii=False))

    async def new_room(self, event: dict):
        """
        Handle new_room event.
        Send new room payload to the client.
        Args:
            event: Event data containing room_id and optional message_id.
        """
        from .utils import format_new_room_payload
        room_id = event.get("room_id")
        message_id = event.get("message_id")
        user_id = str(self.user.id) if hasattr(self.user, 'id') else None

        if not room_id:
            logger.error("No room_id provided in new_room event")
            await self.send(text_data=json.dumps({
                "type": "error",
                "data": {"error": "No room_id provided"}
            }, ensure_ascii=False))
            return

        if not user_id:
            logger.error("No user associated with WebSocket consumer")
            await self.send(text_data=json.dumps({
                "type": "error",
                "data": {"error": "No user associated with WebSocket connection"}
            }, ensure_ascii=False))
            return

        logger.info(
            f"Handling new_room event in consumer for room_id={room_id}, user_id={user_id}, message_id={message_id}")

        try:
            payload = await format_new_room_payload(
                room_id=room_id,
                user_id=user_id,
                message_id=message_id,
                base_url=self.scope.get('base_url')
            )
            await self.send(text_data=json.dumps(payload, ensure_ascii=False))
            logger.info(f"Successfully sent new_room event to user {user_id} for room {room_id}")
        except Exception as e:
            logger.error(
                f"Unexpected error in new_room for room {room_id}, user {user_id}: {str(e)}\n{traceback.format_exc()}")
            await self.send(text_data=json.dumps({
                "type": "error",
                "data": {"error": f"Unexpected error in processing new room: {str(e)}"}
            }, ensure_ascii=False))