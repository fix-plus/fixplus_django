from src.parametric.models import Brand


def create_brand(
        *,
        title: str,
        fa_title: str,
        order: int|None = None,
):
    Brand.objects.create(
        title=title,
        fa_title=fa_title,
        order=order
    )