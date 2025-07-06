import uuid

from django.core.validators import FileExtensionValidator
from django.db import models

from src.common.models import BaseModel
from src.media.validators import FileSizeValidator, ImageSizeValidator
from src.authentication.models import User
from src.geo.models.address import Address


def upload_image_avatar(instance, filename):
    return 'images/avatar/{filename}.{format}'.format( filename=str(uuid.uuid4()), format=filename.split(".")[-1])


class Profile(BaseModel):
    class Gender(models.TextChoices):
        FEMALE = 'FEMALE', 'Female'
        MALE = 'MALE', 'Male'

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False,)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    national_code = models.CharField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=Gender.choices, null=True, blank=True)
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.CASCADE,)
    description = models.TextField(blank=True, null=True)
    avatar = models.ImageField(
        upload_to=upload_image_avatar,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            FileSizeValidator(min_size=1, max_size=10 * 1024 * 1024),
            ImageSizeValidator(max_height=4000, min_height=1, max_width=3000, min_width=1)
        ],
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.mobile}"





