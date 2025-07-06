from django.db import models

from src.common.models import BaseModel
from src.customer.models import Customer


class CustomerPinMessage(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.customer} - {self.description}"

