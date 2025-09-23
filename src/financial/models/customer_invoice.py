from django.utils.translation import gettext_lazy as _
from django.db import models

from src.common.models import BaseModel
from src.parametric.models import WarrantyPeriod
from src.service.models.service import Service



class CustomerInvoice(BaseModel):
    service = models.OneToOneField(Service, null=False, blank=False, on_delete=models.CASCADE, related_name='customer_invoice')
    warranty_period = models.ForeignKey(WarrantyPeriod, null=True, blank=True, on_delete=models.PROTECT)
    warranty_description = models.TextField(null=True, blank=True)
    discount_amount = models.PositiveBigIntegerField(null=False, blank=False, default=0)
    wage_cost = models.PositiveBigIntegerField(null=False, blank=False)
    deadheading_cost = models.PositiveBigIntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.service}"