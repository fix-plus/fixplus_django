from django.db import models

from src.common.models import BaseModel


class DeviceType(BaseModel):
    title = models.CharField(max_length=100, null=False)
    fa_title = models.CharField(max_length=100, null=False)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title}-{self.fa_title}"