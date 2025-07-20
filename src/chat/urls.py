from django.urls import path

from src.chat.apis.history import ChatMessageHistoryApi
from src.chat.apis.status import UnReadChatMessagesCountApi

urlpatterns = [
    path('history/<uuid:deal_offer_id>/', ChatMessageHistoryApi.as_view(), name='chat-message-history'),

    path('status/unread-count/<uuid:deal_offer_id>/', UnReadChatMessagesCountApi.as_view(), name='unread-chat-message-count'),
]