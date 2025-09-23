from src.parametric.models import WarrantyPeriod


def search_warranty_period_list(
        time_unit:str|None=None,
        duration:str|None=None,
):
    queryset = WarrantyPeriod.objects.all()

    if time_unit:
        queryset = queryset.filter(time_unit=time_unit)

    if duration:
        queryset = queryset.filter(duration=duration)

    return queryset


def get_warranty_period(*, id: str) -> WarrantyPeriod:
    try:
        return WarrantyPeriod.objects.get(id=id)
    except WarrantyPeriod.DoesNotExist:
        return None