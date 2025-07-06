from django.db import models

from src.common.models import BaseModel


class Rating(BaseModel):
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)

    def __str__(self):
        return f"{self.title}"