from django.contrib import admin

from src.chat.models import ChatMembership
from unfold.admin import ModelAdmin


@admin.register(ChatMembership)
class ChatMembershipAdmin(ModelAdmin):
    list_display = [
        "id",
    ]