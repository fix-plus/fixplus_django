from django.db.models import Q

from src.authentication.models import User


def get_counterpart_user(
    *,
    role_list: str = None,
    full_name: str =None,
    exclude_user_id: str = None,
    **kwargs,
) -> User:
    queryset = User.objects.filter(Q(is_active=True, is_verified_mobile=True), Q(groups__name='SUPER_ADMIN') | Q(groups__name='ADMIN') | Q(groups__name='TECHNICIAN'))
    queryset = queryset.exclude(id=exclude_user_id)

    if role_list:
        role_list = role_list.split(",") if isinstance(role_list, str) else role_list
        queryset = queryset.filter(groups__name__in=role_list).distinct()

    if full_name:
        queryset = queryset.filter(profile__full_name__icontains=full_name)

    return queryset