import uuid

from django.db import models
from django.db.models.query import F, Q
from django.utils import timezone


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    created_by = models.ForeignKey(
        'authentication.user',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='%(class)s_created_by'
    )
    created_at = models.DateTimeField(
        db_index=True,
        default=timezone.now
    )
    updated_by = models.ForeignKey(
        'authentication.user',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='%(class)s_updated_by'
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True



