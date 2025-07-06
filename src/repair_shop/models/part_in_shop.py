from django.db import models

from src.common.models import BaseModel
from src.customer.models import Customer
from src.service.models.service import Service
from src.authentication.models import User


class PartInShop(BaseModel):
    class Status(models.TextChoices):
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'

    status = models.CharField(max_length=11, choices=Status.choices, default='in_progress')
    job = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='parts_in_shop', null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='parts_in_shop', null=True, blank=True)
    technician = models.ForeignKey(User, on_delete=models.PROTECT, related_name='parts_in_shop', null=True, blank=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.title}"
