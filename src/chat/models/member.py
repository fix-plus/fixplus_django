import uuid

from django.db import models
from django_mongodb_backend import fields


class ChatMembership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    room_id = models.UUIDField(null=True, blank=True)
    user_id = models.UUIDField(null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        indexes = [
            models.Index(fields=["room_id"]),
            models.Index(fields=["user_id"]),
        ]
        ordering = ['joined_at']

    def __str__(self):
        return f"ChatMembership {self.id}"