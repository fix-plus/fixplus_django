# from django.db.models import UUIDField
#
# from fixplus.upload.models import UploadAvatarMedia
#
#
# # Database Business Logic ==============================================================================================
# def get_upload_avatar_media(id:str) -> UploadAvatarMedia:
#     if not UploadAvatarMedia.objects.filter(id=id).exists(): raise Exception(f"media with this id {id} not found.")
#     return UploadAvatarMedia.objects.get(id=id)