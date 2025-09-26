from azbankgateways.models import Bank, PaymentStatus
from django.db import models

from src.authentication.models import User
from src.common.models import BaseModel
from src.service.models import Service


class CustomerPayment(BaseModel):
    service = models.ForeignKey(Service, on_delete=models.PROTECT, null=False, blank=False, related_name='customer_payments')
    technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='customer_payments')

    cheque_amount = models.PositiveBigIntegerField(null=True, blank=True)
    cash_amount = models.PositiveBigIntegerField(null=True, blank=True)
    card_to_card_amount = models.PositiveBigIntegerField(null=True, blank=True)
    online_amount = models.PositiveBigIntegerField(null=True, blank=True)
    online_bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True, blank=True, related_name='customer_payments')
    online_phone_number = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.service}'

    def total_pays(self):
        online_amount = self.online_amount or 0 if self.online_bank.status == PaymentStatus.COMPLETE else 0
        total = (self.cash_amount or 0 + self.cheque_amount or 0 + self.card_to_card_amount or 0 + online_amount)
        return total