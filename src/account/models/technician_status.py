from django.db import models

from src.common.models import SoftDeleteBaseModel, BaseModel
from src.media.models import UploadServiceCardMedia
from src.parametric.models import Brand, Rating
from src.authentication.models import User


class TechnicianStatus(BaseModel, SoftDeleteBaseModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('in_holiday', 'In Holiday'),
        ('in_debt', 'In Debt'),
    ]

    user = models.ForeignKey(
        User,
        null=False,
        on_delete=models.CASCADE,
        related_name='technician_statuses',
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        default='active',
        max_length=20,
        blank=False,
        null=False,
    )

    def __str__(self):
        return f"{self.user.profile.full_name}"
