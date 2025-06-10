from django.db import models

from src.common.models import BaseModel
from src.authentication.models import User


class UserLocationTracker(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='location_trackers')
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.user} - {self.latitude} - {self.longitude}'