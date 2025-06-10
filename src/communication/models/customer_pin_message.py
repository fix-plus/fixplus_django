from django.db import models

from src.authentication.models import User
from src.common.models import BaseModel, SoftDeleteBaseModel
from src.customer.models import Customer


class CustomerPinMessage(BaseModel, SoftDeleteBaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    is_seen = models.BooleanField(default=False)
    seen_at = models.DateTimeField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.customer} - {self.title}"

