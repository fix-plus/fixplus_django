from src.parametric.models import WarrantyPeriod


def create_warranty_period(
        *,
        time_unit: str,
        duration: str,
):
    WarrantyPeriod.objects.create(
        time_unit=time_unit,
        duration=duration,
    )