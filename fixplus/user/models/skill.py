from django.db import models

from fixplus.common.models import SoftDeleteBaseModel
from fixplus.parametric.models import DeviceTypeParametric, BrandNameParametric
from fixplus.user.models import BaseUser


class TechnicianSkill(SoftDeleteBaseModel):
    technician = models.ForeignKey(BaseUser, null=False, on_delete=models.CASCADE, related_name='technician_skill_technician')
    device_type = models.ForeignKey(DeviceTypeParametric, null=False, on_delete=models.CASCADE, related_name='technician_skill_device_type')
    brand_names = models.ManyToManyField(BrandNameParametric, blank=True, related_name='technician_skill_brand_name')