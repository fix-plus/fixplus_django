from django.db import models

from src.common.models import SoftDeleteBaseModel, BaseModel
from src.authentication.models import User


class Customer(BaseModel, SoftDeleteBaseModel):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    full_name = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.full_name}"