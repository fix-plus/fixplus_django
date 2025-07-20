import uuid

from django.db import models
from django_mongodb_backend import fields

from src.common.models import BaseModel


class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    room_id = models.UUIDField(null=False, blank=False)
    user_id = models.UUIDField(null=True, blank=True)
    text = models.CharField(max_length=500, null=True, blank=True)
    file_id = models.UUIDField(null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_system_message = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    replied_from_id = models.UUIDField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["room_id"]),
            models.Index(fields=["user_id"]),
        ]
        ordering = ['timestamp']

    def __str__(self):
        return f"Message {self.id} in Room {self.room_id}"