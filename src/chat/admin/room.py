from django.contrib import admin

from src.chat.models import ChatRoom
from unfold.admin import ModelAdmin


@admin.register(ChatRoom)
class ChatRoomAdmin(ModelAdmin):
    list_display = [
        "id",
    ]