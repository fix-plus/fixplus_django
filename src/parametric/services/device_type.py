from src.parametric.models import DeviceType


def create_device_type(
        *,
        title: str,
        fa_title: str,
        order: int|None = None,
):
    DeviceType.objects.create(
        title=title,
        fa_title=fa_title,
        order=order
    )