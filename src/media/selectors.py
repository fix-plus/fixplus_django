from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from src.media.models import UploadIdentifyDocumentMedia, UploadServiceCardMedia


def get_upload_identify_document_media(id: str) -> UploadIdentifyDocumentMedia:
    try:
        return UploadIdentifyDocumentMedia.objects.get(id=id)
    except UploadIdentifyDocumentMedia.DoesNotExist:
        raise ObjectDoesNotExist(_("Media file not found."))


def get_upload_service_card_media(id: str) -> UploadServiceCardMedia:
    try:
        return UploadServiceCardMedia.objects.get(id=id)
    except UploadServiceCardMedia.DoesNotExist:
        raise ObjectDoesNotExist(_("Media file not found."))