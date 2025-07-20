import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from src.chat.services.ws import send_message, mark_message_delivered, mark_message_read
from src.chat.selectors.ws import get_message_by_id
from src.trade.models import DealOffer
from src.chat.models import ChatRoom

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handle WebSocket connection."""
        self.user_id = self.scope["user"].id
        if not self.user_id:
            await self.close()
            return
        # Join user group for status updates
        self.user_group_name = f"user_{self.user_id}"
        await self.channel_layer.group_add(self.user_group_name, self.channel_name)
        # Join groups for all deal offers where the user is either the offerer or the order owner
        deal_offers = await self.get_user_deal_offers()
        for deal_offer in deal_offers:
            group_name = f"deal_offer_{deal_offer.id}"
            await self.channel_layer.group_add(group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        try:
            # Leave user group
            await self.channel_layer.group_discard(self.user_group_name, self.channel_name)
            # Leave deal offer groups
            deal_offers = await self.get_user_deal_offers()
            for deal_offer in deal_offers:
                group_name = f"deal_offer_{deal_offer.id}"
                await self.channel_layer.group_discard(group_name, self.channel_name)
        except:
            pass

    @database_sync_to_async
    def get_user_deal_offers(self):
        """Retrieve all deal offers where the user is either the offerer or the order owner."""
        from django.db.models import Q
        return list(DealOffer.objects.filter(Q(user_id=self.user_id) | Q(order__user_id=self.user_id)))

    async def receive(self, text_data):
        """Receive and process WebSocket messages."""
        try:
            data = json.loads(text_data)
            action = data.get("action")

            if action == "send_message":
                message = await database_sync_to_async(send_message)(
                    sender_id=self.user_id,
                    deal_offer_id=data["deal_offer_id"],
                    text=data.get("text"),
                    file_id=data.get("file_id"),
                    replied_to_id=data.get("replied_to_id")
                )

            elif action == "mark_delivered":
                await database_sync_to_async(mark_message_delivered)(
                    message_id=data["message_id"],
                    receiver_id=self.user_id
                )

            elif action == "mark_read":
                await database_sync_to_async(mark_message_read)(
                    message_id=data["message_id"],
                    user_id=self.user_id
                )

        except json.JSONDecodeError:
            await self.send(text_data=str(_("Invalid JSON format")))
        except ValidationError as e:
            error_message = str(e).replace("['", "").replace("']", "")
            await self.send(text_data=str(_(error_message)))
        except Exception as e:
            print(e)
            await self.send(text_data=str(_("An unexpected error occurred")))

    async def chat_message(self, event):
        """Send a new message to the client."""
        message = await database_sync_to_async(get_message_by_id)(event["message_id"])
        room = await database_sync_to_async(ChatRoom.objects.get)(id=message.room_id)
        is_sent = str(message.user_id) == str(self.user_id)
        await self.send(text_data=json.dumps({
            "type": "new_message",
            "deal_offer_id": str(room.deal_offer_id),
            "message": {
                "id": str(message.id),
                "sender": str(message.user_id),
                "text": message.text,
                "file_id": str(message.file_id) if message.file_id else None,
                "replied_from_id": str(message.replied_from_id) if message.replied_from_id else None,
                "is_delivered": message.is_delivered,
                "is_read": message.is_read,
                "timestamp": int(message.timestamp.timestamp()),
                "is_sent": is_sent
            }
        }, ensure_ascii=False))

    async def message_status(self, event):
        """Send message status update to the client."""
        message = await database_sync_to_async(get_message_by_id)(event["message_id"])
        room = await database_sync_to_async(ChatRoom.objects.get)(id=message.room_id)
        await self.send(text_data=json.dumps({
            "type": "message_status",
            "deal_offer_id": str(room.deal_offer_id),
            "message_id": event["message_id"],
            "status": event["status"]
        }, ensure_ascii=False))