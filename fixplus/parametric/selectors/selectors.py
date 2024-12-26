from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from fixplus.parametric.models import TimingSettingParametric, BrandNameParametric, DeviceTypeParametric


def get_timing_setting() -> TimingSettingParametric:
    try:
        return TimingSettingParametric.objects.first()
    except TimingSettingParametric.DoesNotExist:
        raise ObjectDoesNotExist(_("The configuration parameter was not found, please contact the admin."))


def get_brand_name(
    *,
    id:str
):
    return


def search_brand_name_list(
        title:str|None=None,
        fa_title:str|None=None,
):
    queryset = BrandNameParametric.objects.all()

    if title:
        queryset = queryset.filter(title__icontains=title)

    if fa_title:
        queryset = queryset.filter(fa_title__icontains=fa_title)

    return queryset


def search_device_type_list(
        title: str | None = None,
        fa_title: str | None = None,
):
    queryset = DeviceTypeParametric.objects.all()

    if title:
        queryset = queryset.filter(title__icontains=title)

    if fa_title:
        queryset = queryset.filter(fa_title__icontains=fa_title)

    return queryset