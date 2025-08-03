from django.urls import path

from src.chat.apis.chat import ChatRoomListApi
from src.chat.apis.counterpart_user import ChatCounterpartUserApi
from src.chat.apis.history import ChatMessageHistoryApi
# from src.chat.apis.status import UnReadChatMessagesCountApi

urlpatterns = [
    path('rooms/', ChatRoomListApi.as_view(), name='room-list'),
    path('history/<uuid:room_id>/', ChatMessageHistoryApi.as_view(), name='chat-message-history'),
    path('counterparts/', ChatCounterpartUserApi.as_view(), name='counterpart-list'),
    # path('status/unread-count/<uuid:room_id>/', UnReadChatMessagesCountApi.as_view(), name='unread-chat-message-count'),
]