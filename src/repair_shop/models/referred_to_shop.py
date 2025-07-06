from django.db import models

from src.common.models import BaseModel
from src.customer.models import Customer, CustomerContactNumber
from src.service.models.service import Service
from src.parametric.models import DeviceType, Brand
from src.geo.models.address import Address
from src.payment.models import CustomerPayment


class ReferredToShopJob(BaseModel):
    service = models.ForeignKey(Service, null=False, blank=False, on_delete=models.CASCADE)
    is_full_device = models.BooleanField(default=False, blank=False, null=False)
    estimate_back_at = models.DateTimeField(null=True, blank=True)
    customer_mobile_number = models.ForeignKey(CustomerContactNumber, null=False, blank=False, on_delete=models.CASCADE)
    pre_pay = models.ForeignKey(CustomerPayment, null=True, blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, null=False, blank=False)

    def __str__(self):
        return f"{self.service.brand_name}-{self.service.device_type}"