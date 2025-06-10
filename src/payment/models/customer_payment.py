from django.db import models
from django.db.models import Sum

from src.common.models import BaseModel, SoftDeleteBaseModel
from src.customer.models import Customer
from src.payment.models import ChequePay, CashPay, CardToCardPay, OnlinePay


class CustomerPayment(BaseModel, SoftDeleteBaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    cheque = models.ManyToManyField(ChequePay, blank=True)
    cash = models.ManyToManyField(CashPay, blank=True)
    card_to_card = models.ManyToManyField(CardToCardPay, blank=True)
    online = models.ManyToManyField(OnlinePay, blank=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.customer.full_name}'

    def total_pays(self):
        total_cheque = self.cheque.filter(is_paid=True).aggregate(Sum('amount'))['amount__sum'] or 0
        total_cash = self.cash.filter(is_paid=True).aggregate(Sum('amount'))['amount__sum'] or 0
        total_card_to_card = self.card_to_card.filter(is_paid=True).aggregate(Sum('amount'))['amount__sum'] or 0
        total_online = self.online.filter(is_paid=True).aggregate(Sum('amount'))['amount__sum'] or 0

        total = (total_cheque + total_cash + total_card_to_card + total_online)
        return total