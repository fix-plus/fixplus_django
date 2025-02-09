from django.db import models

from src.common.models import BaseModel, SoftDeleteBaseModel
from src.customer.models import Customer, CustomerContactNumber
from src.service.models.job import Job
from src.parametric.models import DeviceType, Brand
from src.geo.models.address import Address
from src.payment.models import CustomerPayment


class InvoicingJob(BaseModel, SoftDeleteBaseModel):
    job = models.ForeignKey(
        Job,
        null=False,
        blank=False,
        on_delete=models.PROTECT
    )
    warranty_month_length = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    deadheading_cost = models.PositiveBigIntegerField(
        null=False,
        blank=False,
    )
    wage_cost = models.PositiveBigIntegerField(
        null=False,
        blank=False,
    )
    technician_description = models.TextField(
        null=False,
        blank=False,
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