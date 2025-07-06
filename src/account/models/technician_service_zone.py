from django.db import models

from src.common.authentication_backends import User
from src.common.models import BaseModel


class TechnicianServiceZone(BaseModel):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='technician_service_zone')
    zone = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return f"{self.user - self.zone}"