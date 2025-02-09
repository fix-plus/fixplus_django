from django.db import models

from src.common.models import BaseModel, SoftDeleteBaseModel
from src.customer.models import Customer


class ChequePay(BaseModel, SoftDeleteBaseModel):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name='cheque_pays'
    )
    amount = models.PositiveBigIntegerField(
        null=False,
        blank=False,
    )
    is_paid = models.BooleanField(
        default=False,
        null=False,
        blank=False
    )
    cheque_id = models.CharField(
        max_length=36,
        null=True,
        blank=True,
        unique=True
    )
    due_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.amount)