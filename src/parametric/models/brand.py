from django.db import models

from src.common.models import BaseModel


class Brand(BaseModel):
    title = models.CharField(max_length=100, null=False)
    fa_title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True, blank=True,)
    fa_description = models.TextField(null=True, blank=True,)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return f"{self.title}-{self.fa_title}"