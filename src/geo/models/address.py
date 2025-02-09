from django.db import models

from src.authentication.models import User
from src.common.models import BaseModel, SoftDeleteBaseModel


class Address(BaseModel, SoftDeleteBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', null=True, blank=True)
    address = models.TextField(null=False, blank=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.address