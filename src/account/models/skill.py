from django.db import models

from src.common.models import SoftDeleteBaseModel, BaseModel
from src.parametric.models import DeviceType, Brand
from src.authentication.models import User


class TechnicianSkill(BaseModel, SoftDeleteBaseModel):
    user = models.ForeignKey(
        User,
        null=False,
        on_delete=models.CASCADE,
        related_name='technician_skills',
    )
    device_type = models.ForeignKey(
        DeviceType,
        null=False,
        on_delete=models.CASCADE,
    )
    brand_names = models.ManyToManyField(
        Brand,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.profile.full_name}"
