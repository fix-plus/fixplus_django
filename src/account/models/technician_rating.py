from django.db import models

from src.common.models import SoftDeleteBaseModel, BaseModel
from src.media.models import UploadServiceCardMedia
from src.parametric.models import Brand, Rating
from src.authentication.models import User


class TechnicianRating(BaseModel, SoftDeleteBaseModel):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='technician_ratings')
    rating = models.ManyToManyField(Rating, blank=False, through='TechnicianRatingValue')

    def __str__(self):
        return f"{self.user.profile.full_name}"


class TechnicianRatingValue(BaseModel, SoftDeleteBaseModel):
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    technician_rating = models.ForeignKey(TechnicianRating, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(null=False, blank=False)
