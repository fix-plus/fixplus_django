from django.db import models

from src.common.models import BaseModel, SoftDeleteBaseModel
from src.customer.models import Customer


class CashPay(BaseModel, SoftDeleteBaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='cash_pays')
    amount = models.PositiveBigIntegerField(null=False, blank=False)
    is_paid = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.amount)