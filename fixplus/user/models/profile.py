import uuid

from django.core.validators import FileExtensionValidator
from django.db import models

from fixplus.common.models import BaseModel
from fixplus.upload.validators import FileSizeValidator, ImageSizeValidator
from fixplus.user.models import BaseUser
from fixplus.user.utils import generate_referral_code


def upload_image_avatar(instance, filename):
    return 'images/avatar/{filename}.{format}'.format( filename=str(uuid.uuid4()), format=filename.split(".")[-1])


class Profile(BaseModel):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    user = models.OneToOneField(BaseUser, on_delete=models.PROTECT)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    national_code = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    address = models.TextField(blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True)
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


class LandLineNumber(BaseModel):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    number = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.ref_code = generate_referral_code(length=6)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.mobile}"


class MobileNumber(BaseModel):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    number = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.ref_code = generate_referral_code(length=6)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.mobile}"

