from django.db import models

from src.common.models import SoftDeleteBaseModel, BaseModel
from src.media.models import UploadServiceCardMedia
from src.parametric.models import Brand
from src.authentication.models import User


class TechnicianServiceCard(BaseModel, SoftDeleteBaseModel):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='technician_service_cards')
    brand = models.ForeignKey(Brand, blank=True, on_delete=models.CASCADE)
    photo = models.ForeignKey(UploadServiceCardMedia, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.profile.full_name}"
