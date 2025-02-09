from django.db import models

from src.common.models import BaseModel, SoftDeleteBaseModel
from src.customer.models import Customer, CustomerContactNumber
from src.service.models.job import Job
from src.parametric.models import DeviceType, Brand
from src.geo.models.address import Address
from src.payment.models import CustomerPayment


class ReferredToShopJob(BaseModel, SoftDeleteBaseModel):
    job = models.ForeignKey(
        Job,
        null=False,
        blank=False,
        on_delete=models.PROTECT
    )
    is_full_device = models.BooleanField(
        default=False,
        blank=False,
        null=False
    )
    estimate_back_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    customer_mobile_number = models.ForeignKey(
        CustomerContactNumber,
        null=False,
        blank=False,
        on_delete=models.PROTECT
    )
    pre_pay = models.ForeignKey(
        CustomerPayment,
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
    )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.job.brand_name}-{self.job.device_type}"