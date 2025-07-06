from django.db import models

from src.common.models import BaseModel
from src.customer.models import Customer


class OnlinePay(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='online_pays')
    amount = models.PositiveBigIntegerField(null=False, blank=False)
    is_paid = models.BooleanField(default=False, null=False, blank=False)
    order_id = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.amount)