from django.db import models

from src.authentication.models import User
from src.common.models import BaseModel, SoftDeleteBaseModel
from src.customer.models import Customer


class AdminPinMessageOfTechnician(BaseModel, SoftDeleteBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} - {self.description}"

