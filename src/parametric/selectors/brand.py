from src.parametric.models import Brand


def search_brand_name_list(
        title:str|None=None,
        fa_title:str|None=None,
):
    queryset = Brand.objects.all()

    if title:
        queryset = queryset.filter(title__icontains=title)

    if fa_title:
        queryset = queryset.filter(fa_title__icontains=fa_title)

    return queryset