from typing import Optional

from django.contrib.auth.models import Group
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, OuterRef, Subquery
from django.utils.translation import gettext_lazy as _

from src.account.models import UserRegistryRequest, TechnicianStatus
from src.common.custom_exception import CustomAPIException
from src.authentication.models import User


# Cache ----------------------------------------------------------------------------------------------------------------
def get_cache_verification_mobile_otp(mobile: str) -> bool|None:
    cache_key = mobile + "_verification_mobile_otp"
    cache_value = cache.get(cache_key)
    return cache_value


# Db -------------------------------------------------------------------------------------------------------------------
def get_user(id: Optional[str] = None, mobile: Optional[str] = None) -> User:
    try:
        if mobile:
            return User.objects.get(mobile=mobile)
        if id:
            return User.objects.get(id=id)
    except ObjectDoesNotExist:
        raise CustomAPIException(_("User not found."))


def search_user_list(
    mobile: str = None,
    registry_status: list | None = None,
    technician_status: list | None = None,
    full_name: str | None = None,
    group: list | None = None,
    sort_by: str | None = None,
    order: str = 'desc'  # Default to descending order
) -> User :
    # Start with the User  queryset
    queryset = User.objects.all()

    # Filter by mobile if provided
    if mobile:
        queryset = queryset.filter(mobile__startswith=mobile)

    # Filter by registry status if provided
    if registry_status:
        registry_status = registry_status.split(',')

        # Get the latest registry request for each user
        latest_requests = UserRegistryRequest.objects.filter(
            user=OuterRef('pk')
        ).order_by('-created_at')

        # Annotate the queryset with the latest registry request status
        queryset = queryset.annotate(
            latest_request_status=Subquery(latest_requests.values('status')[:1])
        ).filter(
            latest_request_status__in=registry_status
        )

    # Filter by registry status if provided
    if technician_status:
        technician_status = technician_status.split(',')

        # Get the latest registry request for each user
        latest_status = TechnicianStatus.objects.filter(
            user=OuterRef('pk')
        ).order_by('-created_at')

        # Annotate the queryset with the latest registry request status
        queryset = queryset.annotate(
            latest_technician_status=Subquery(latest_status.values('status')[:1])
        ).filter(
            latest_technician_status__in=technician_status
        )

    # Join with Profile to filter by full_name if provided
    if full_name:
        queryset = queryset.filter(profile__full_name__istartswith=full_name)

    # Filter by group if provided (assuming group is a list of account IDs)
    if group:
        group = group.split(',')
        # Create a Q object for each group and combine them with OR
        q_objects = Q()
        for g in group:
            q_objects |= Q(groups__name=g)

        # Filter the queryset using the combined Q object
        queryset = queryset.filter(q_objects).annotate(group_count=Count('groups')).distinct()

    # Determine the order direction
    order_prefix = '-' if order == 'desc' else ''

    # Sort the results if sort_by is provided
    if sort_by:
        if sort_by in ['created_at', 'last_online', 'request_register_datetime']:
            queryset = queryset.order_by(f"{order_prefix}{sort_by}")
        else:
            raise ValueError("Invalid sort_by value. Must be one of: 'created_at', 'last_online', 'request_register_datetime'.")

    return queryset


def is_exist_user(
        mobile:str = None,
        id: str = None
) -> bool:
    if mobile is not None: return User.objects.filter(mobile=mobile).exists()
    if id is not None: return User.objects.filter(id=id).exists()
    else:
        raise CustomAPIException()


def is_verified_mobile(mobile: str = None,) -> bool:
    if User.objects.filter(mobile=mobile, is_verified_mobile=True).exists(): return True
    return False


def get_tokens_user(*, mobile:str=None, user:User=None) -> dict:
    global db_user

    if mobile: db_user = User.objects.filter(mobile=mobile)
    if user:db_user = user
    if not user and not db_user.exists(): raise CustomAPIException(_("User not found."))

    db_user = db_user.first() if user is None else db_user
    if mobile and not is_verified_mobile(mobile=mobile): raise CustomAPIException(_("User not verified, please verified mobile first."))
    if user and not user.is_verified_mobile: raise CustomAPIException(_("User not verified, please verified mobile first."))

    tokens = db_user.get_tokens()
    groups = list(db_user.groups.values_list('name', flat=True))
    permissions = list(db_user.user_permissions.values_list('codename', flat=True))
    return {
        "tokens": tokens,
        "groups": groups,
        "permissions": permissions,
        "is_verified_mobile": db_user.is_verified_mobile,
        "status": db_user.registry_requests.latest('created_at').status if db_user.registry_requests.exists() else None,
    }