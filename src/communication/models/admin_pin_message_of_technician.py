from django.db import models

from src.authentication.models import User
from src.common.models import BaseModel


class AdminPinMessageOfTechnician(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} - {self.description}"

