from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from src.authentication.models import User
from src.common.models import BaseModel
from src.media.models import UploadIdentifyDocumentMedia


class UserRegistryRequest(BaseModel):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        CHECKING = 'CHECKING', 'Checking'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT,)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registry_requests')
    identify_document_photo = models.ForeignKey(UploadIdentifyDocumentMedia, blank=True, null=True, on_delete=models.CASCADE, related_name='identify_document_photo')
    other_identify_document_photos = models.ManyToManyField(UploadIdentifyDocumentMedia, blank=True, related_name='other_identify_document_photos')
    rejected_reason = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Registry Request"
        verbose_name_plural = "Registry Request"
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        # Call the clean method to validate before saving
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}"

