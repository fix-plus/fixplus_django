from django.db import models
from django.db.models import Sum

from src.common.models import BaseModel
from src.payment.models import ChequePay, CashPay, CardToCardPay, OnlinePay
from src.service.models import Service


class CustomerPayment(BaseModel):
    service = models.ForeignKey(Service, on_delete=models.PROTECT, null=False, blank=False, related_name='customer_payments')
    cheque_pay = models.ForeignKey(ChequePay, blank=True, null=True, on_delete=models.PROTECT)
    cash_pay = models.ForeignKey(CashPay, blank=True, null=True, on_delete=models.PROTECT)
    card_to_card_pay = models.ForeignKey(CardToCardPay, blank=True, null=True, on_delete=models.PROTECT)
    online_pay = models.ForeignKey(OnlinePay, blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.service}'

    def total_pays(self):
        total_cheque = self.cheque_pay.filter(is_paid=True).aggregate(Sum('amount'))['amount__sum'] or 0
        total_cash = self.cash_pay.filter(is_paid=True).aggregate(Sum('amount'))['amount__sum'] or 0
        total_card_to_card = self.card_to_card_pay.filter(is_paid=True).aggregate(Sum('amount'))['amount__sum'] or 0
        total_online = self.online_pay.filter(is_paid=True).aggregate(Sum('amount'))['amount__sum'] or 0

        total = (total_cheque + total_cash + total_card_to_card + total_online)
        return total