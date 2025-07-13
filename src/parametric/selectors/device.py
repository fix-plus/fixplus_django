from src.parametric.models import DeviceType


def search_device_type_list(
        title: str | None = None,
        fa_title: str | None = None,
):
    queryset = DeviceType.objects.all()

    if title:
        queryset = queryset.filter(title__icontains=title)

    if fa_title:
        queryset = queryset.filter(fa_title__icontains=fa_title)

    return queryset