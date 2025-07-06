from django.db import models

from src.common.models import BaseModel
from src.customer.models import Customer


class CardToCardPay(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='card_to_card_pays')
    amount = models.PositiveBigIntegerField(null=False, blank=False)
    is_paid = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.amount)