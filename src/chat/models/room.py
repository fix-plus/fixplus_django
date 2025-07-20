import uuid

from django.db import models
from django_mongodb_backend import fields


class ChatRoom(models.Model):
    class Type(models.TextChoices):
        SERVICE = "SERVICE", "Service"
        TECHNICIAN_DIRECT = "TECHNICIAN_DIRECT", "Technician Direct"
        ADMIN_DIRECT = "ADMIN_DIRECT", "Admin Direct"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    type = models.CharField(max_length=30, choices=Type.choices)
    service_id = models.UUIDField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["service_id"]),
        ]
        ordering = ['timestamp']

    def __str__(self):
        return f"Room {self.id} ({self.type})"