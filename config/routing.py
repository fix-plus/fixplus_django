from django.urls import path

from src.chat.consumers import ChatWebSocketConsumer

websocket_urlpatterns = [
    path("ws/chat/", ChatWebSocketConsumer.as_asgi()),
]