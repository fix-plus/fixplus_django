from django.contrib import admin
from unfold.contrib.filters.admin import FieldTextFilter

from src.chat.models import ChatMessage
from unfold.admin import ModelAdmin


@admin.register(ChatMessage)
class ChatMessageAdmin(ModelAdmin):
    list_display = [
        "user_id",
        "text",
    ]

    list_filter_submit = True  # Submit button at the bottom of the filter
    list_filter = [
        ("user_id", FieldTextFilter),
    ]