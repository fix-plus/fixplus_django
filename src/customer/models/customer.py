from django.db import models

from src.common.models import BaseModel


class Customer(BaseModel):
    class Gender(models.TextChoices):
        FEMALE = 'FEMALE', 'Female'
        MALE = 'MALE', 'Male'

    full_name = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=Gender.choices)

    def __str__(self):
        return f"{self.full_name}"