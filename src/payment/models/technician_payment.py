from azbankgateways.models import Bank, PaymentStatus
from django.db import models

from src.authentication.models import User
from src.common.models import BaseModel
from src.service.models import Service


class TechnicianPayment(BaseModel):
    technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='technician_payments')

    online_amount = models.PositiveBigIntegerField(null=True, blank=True)
    online_bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True, blank=True, related_name='technician_payments')

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.technician}'