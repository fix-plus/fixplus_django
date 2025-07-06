from django.db import models

from src.common.models import BaseModel
from src.customer.models import Customer, CustomerContactNumber
from src.service.models.service import Service



class ServiceInvoice(BaseModel):
    service = models.ForeignKey(Service, null=False, blank=False, on_delete=models.CASCADE, related_name='invoices')
    warranty_month_length = models.PositiveIntegerField(null=True, blank=True)
    deadheading_cost = models.PositiveBigIntegerField(null=False, blank=False)
    wage_cost = models.PositiveBigIntegerField(null=False, blank=False)
    technician_description = models.TextField(null=False, blank=False)
    is_active = models.BooleanField(default=True, null=False, blank=False)

    def __str__(self):
        return f"{self.service.brand_name}-{self.service.device_type}"