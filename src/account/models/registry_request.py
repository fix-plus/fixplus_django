from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from src.authentication.models import User
from src.common.models import SoftDeleteBaseModel, BaseModel
from src.media.models import UploadIdentifyDocumentMedia


class UserRegistryRequest(BaseModel, SoftDeleteBaseModel):
    DRAFT = 'draft'
    CHECKING = 'checking'
    APPROVED = 'approved'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (CHECKING, 'Checking'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    status = models.CharField(
        max_length=12,
        blank=False,
        null=False,
        choices=STATUS_CHOICES,
        default='draft',
    )
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

