from django.db import models

from src.common.models import BaseModel, SoftDeleteBaseModel
from src.customer.models import Customer, CustomerContactNumber
from src.service.models.service import Service
from src.parametric.models import DeviceType, Brand
from src.geo.models.address import Address
from src.payment.models import CustomerPayment


class ServicePayment(BaseModel, SoftDeleteBaseModel):
    service = models.ForeignKey(Service, null=False, blank=False, on_delete=models.CASCADE, related_name='payments')
    customer_payment = models.ForeignKey(CustomerPayment, null=True, blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, null=False, blank=False)

    def __str__(self):
        return f"{self.service.brand_name}-{self.service.device_type}"