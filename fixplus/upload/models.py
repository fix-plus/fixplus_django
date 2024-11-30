# import uuid
#
# from django.core.validators import FileExtensionValidator
# from django.db import models
# from thumbnails.fields import ImageField
#
# from fixplus.common.models import BaseModel
# from fixplus.upload.validators import FileSizeValidator, ImageSizeValidator
# from fixplus.user.models import BaseUser
#
#
# def upload_image_avatar(instance, filename):
#     return 'images/avatar/{filename}.{format}'.format( filename=str(uuid.uuid4()), format=filename.split(".")[-1])
#
#
# class UploadAvatarMedia(BaseModel):
#     user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
#     image = models.ImageField(
#         upload_to=upload_image_avatar,
#         validators=[
#             FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
#             FileSizeValidator(min_size=1, max_size=10 * 1024 * 1024),
#             ImageSizeValidator(max_height=4000, min_height=1, max_width=3000, min_width=1)
#         ],
#         null=True,
#         blank=True,
#     )
#
#     class Meta:
#         verbose_name = "Avatar Medias"
#         verbose_name_plural = "Avatar Medias"
#
#     def __str__(self):
#         return f"{self.id}"