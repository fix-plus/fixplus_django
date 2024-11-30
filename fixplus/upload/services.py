# from django.db.models import ImageField, UUIDField, FileField
#
# from fixplus.upload.models import UploadAvatarMedia
# from fixplus.users.models import BaseUser
#
#
# def create_upload_avatar_media(*, user:BaseUser, id: str=None, image: ImageField | None = None) -> UploadAvatarMedia:
#     if image:
#         return UploadAvatarMedia.objects.create(user= user, id=id, image=image)
#     else:
#         raise Exception("Unknown error occurred.")