from django.db import models

from src.common.models import BaseModel
from src.service.models import Service


class ServiceHistory(BaseModel):
    class EventType(models.TextChoices):
        CREATE = "CREATE", "Create"
        UPDATE = "UPDATE", "Update"
        DELETE = "DELETE", "Delete"


    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="histories")

    # Fields
    event_type = models.CharField(max_length=20, choices=EventType.choices)
    previous_status = models.CharField(max_length=20, choices=Service.Status.choices, null=True, blank=True)
    new_status = models.CharField(max_length=20, choices=Service.Status.choices, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True, help_text="Optional remarks or notes about the event.")

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["service", "created_at"]),
        ]

    def __str__(self) -> str:
        """String representation of the ServiceHistory instance."""
        if self.event_type == self.EventType.CREATE:
            return f"Service {self.service.id}: Created with status {self.new_status}"
        elif self.event_type == self.EventType.DELETE:
            return f"Service {self.service.id}: Deleted (last status: {self.previous_status})"
        return f"Service {self.service.id}: {self.previous_status} → {self.new_status}"

    def save(self, *args, **kwargs):
        """Override save to validate status fields based on event type."""
        if self.event_type == self.EventType.UPDATE and self.previous_status == self.new_status:
            raise ValueError("Previous and new status must differ for update events.")
        super().save(*args, **kwargs)