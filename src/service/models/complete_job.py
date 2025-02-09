from django.db import models

from src.common.models import BaseModel, SoftDeleteBaseModel
from src.customer.models import Customer, CustomerContactNumber
from src.service.models.job import Job
from src.parametric.models import DeviceType, Brand
from src.geo.models.address import Address
from src.payment.models import CustomerPayment


class CompleteInvoiceJob(BaseModel, SoftDeleteBaseModel):
    job = models.ForeignKey(
        Job,
        null=False,
        blank=False,
        on_delete=models.PROTECT
    )
    technician_detail_description = models.TextField(
        null=True,
        blank=True
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