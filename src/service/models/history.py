from django.db import models

from src.common.models import BaseModel
from src.service.models import Service


class ServiceHistory(BaseModel):
    """
    Records lifecycle events (create, update, delete) for a Service instance.

    Attributes:
        service: The related Service instance.
        event_type: The type of event (create, update, delete).
        previous_status: The status before the event (if applicable).
        new_status: The status after the event (if applicable).
        remarks: Optional notes about the event.
    """

    # Event types
    EVENT_CREATE = "create"
    EVENT_UPDATE = "update"
    EVENT_DELETE = "delete"
    EVENT_CHOICES = [
        (EVENT_CREATE, "Created"),
        (EVENT_UPDATE, "Updated"),
        (EVENT_DELETE, "Deleted"),
    ]

    # Relationships
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="histories",
        help_text="The service this history entry pertains to.",
    )

    # Fields
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_CHOICES,
        help_text="The type of event that occurred.",
    )
    previous_status = models.CharField(
        max_length=20,
        choices=Service.STATUS_CHOICES,
        null=True,
        blank=True,
        help_text="The previous status of the service (if applicable).",
    )
    new_status = models.CharField(
        max_length=20,
        choices=Service.STATUS_CHOICES,
        null=True,
        blank=True,
        help_text="The new status of the service (if applicable).",
    )
    remarks = models.TextField(
        null=True,
        blank=True,
        help_text="Optional remarks or notes about the event.",
    )

    class Meta:
        verbose_name = "Service History"
        verbose_name_plural = "Service Histories"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["service", "created_at"]),
        ]

    def __str__(self) -> str:
        """String representation of the ServiceHistory instance."""
        if self.event_type == self.EVENT_CREATE:
            return f"Service {self.service.id}: Created with status {self.new_status}"
        elif self.event_type == self.EVENT_DELETE:
            return f"Service {self.service.id}: Deleted (last status: {self.previous_status})"
        return f"Service {self.service.id}: {self.previous_status} → {self.new_status}"

    def save(self, *args, **kwargs):
        """Override save to validate status fields based on event type."""
        if self.event_type == self.EVENT_UPDATE and self.previous_status == self.new_status:
            raise ValueError("Previous and new status must differ for update events.")
        super().save(*args, **kwargs)