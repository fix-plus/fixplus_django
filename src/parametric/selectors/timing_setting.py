from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from src.parametric.models import TimingSetting


def get_timing_setting() -> TimingSetting:
    try:
        return TimingSetting.objects.first()
    except TimingSetting.DoesNotExist:
        raise ObjectDoesNotExist(_("The configuration parameter was not found, please contact the admin."))