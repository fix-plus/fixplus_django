import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .group_manager import join_user_groups, leave_user_groups
from .event_dispatcher import dispatch_event
from .event_schema import InputEvent, OutputEvent
from ..services.channel_storage import channel_storage


class ChatWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Handle WebSocket connection.
        Authenticate user and join relevant groups.
        """
        self.user = self.scope["user"]

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
                "error": str(_("Authentication required"))
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
            await self.send(text_data=json.dumps({
                "type": "error",
                "error": str(_("Connection failed: %(error)s") % {"error": str(e)})
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
            print(f"Error during disconnect: {e}")

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
            await self.send(text_data=json.dumps({
                "type": "error",
                "error": str(_("Invalid JSON format"))
            }, ensure_ascii=False))
        except ValidationError as e:
            error_message = str(e).replace("['", "").replace("']", "")
            await self.send(text_data=json.dumps({
                "type": "error",
                "error": str(_(error_message))
            }, ensure_ascii=False))
        except Exception as e:
            await self.send(text_data=json.dumps({
                "type": "error",
                "error": str(_("An unexpected error occurred: %(error)s") % {"error": str(e)})
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
            payload = await format_message_payload(event["message_id"], self.user.id)
            await self.send(text_data=json.dumps({
                "type": "new_message",
                **payload
            }, ensure_ascii=False))
        except Exception as e:
            await self.send(text_data=json.dumps({
                "type": "error",
                "error": str(_("Failed to process message: %(error)s") % {"error": str(e)})
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
            await self.send(text_data=json.dumps({
                "type": "message_status",
                **payload
            }, ensure_ascii=False))
        except Exception as e:
            await self.send(text_data=json.dumps({
                "type": "error",
                "error": str(_("Failed to process status: %(error)s") % {"error": str(e)})
            }, ensure_ascii=False))