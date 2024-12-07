from django.core.exceptions import ObjectDoesNotExist

from fixplus.upload.models import UploadIdentifyDocumentMedia


# Database Business Logic ==============================================================================================
def get_upload_identify_document_media(id: str) -> UploadIdentifyDocumentMedia:
    try:
        return UploadIdentifyDocumentMedia.objects.get(id=id)
    except UploadIdentifyDocumentMedia.DoesNotExist:
        raise ObjectDoesNotExist(f"Media with ID {id} not found.")