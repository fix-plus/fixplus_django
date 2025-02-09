from django.db import models

from src.common.models import BaseModel, SoftDeleteBaseModel
from src.customer.models import Customer
from src.service.models.job import Job
from src.parametric.models import DeviceType, Brand
from src.geo.models.address import Address


class AssignedJob(BaseModel, SoftDeleteBaseModel):
    job = models.ForeignKey(
        Job,
        null=False,
        blank=False,
        on_delete=models.PROTECT
    )
    technician = models.ForeignKey(
        Customer,
        null=True,
        blank=True,
        related_name="technician",
        on_delete=models.PROTECT
    )
    deadline_accepting_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
    )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.technician.full_name} : {self.job.brand_name}-{self.job.device_type}"