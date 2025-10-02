from django.db import models

from src.common.models import BaseModel
from src.service.models.service import Service


class InvoiceDeductionItem(BaseModel):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='invoice_deduction_items', null=False, blank=False)
    description = models.CharField(null=False, blank=False)
    cost = models.PositiveBigIntegerField(null=False, blank=False)
    quantity = models.PositiveIntegerField(null=False, blank=False, default=1)

    def __str__(self):
        return f"{self.service}"
