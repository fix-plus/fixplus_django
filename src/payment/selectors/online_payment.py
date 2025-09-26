from typing import Optional, List
from azbankgateways.models import Bank
from src.order.models import Order
from src.authentication.models import User


def search_payment(
    user: Optional[User] = None,
    order: Optional[Order] = None,
    tracking_code: Optional[str] = None,
    status: Optional[str] = None,
    sort_by: Optional[str] = "created_at",
    order_by: Optional[str] = "desc",
) -> Bank.objects.all().__class__:
    """
    Searches and filters payment records based on provided criteria.

    Args:
        user: Filter by user instance.
        order: Filter by order instance.
        tracking_code: Filter by payment tracking code.
        status: Filter by payment status.
        sort_by: Field to sort by (default: 'created_at').
        order_by: Sort direction ('asc' or 'desc', default: 'desc').

    Returns:
        QuerySet: Filtered and sorted queryset of Bank objects.
    """
    queryset = Bank.objects.select_related('order__user').all()

    if user is not None:
        if not isinstance(user, User):
            raise ValueError("User must be a valid User instance.")
        queryset = queryset.filter(order__user=user)

    if order is not None:
        if not isinstance(order, Order):
            raise ValueError("Order must be a valid Order instance.")
        queryset = queryset.filter(order=order)

    if tracking_code is not None:
        queryset = queryset.filter(tracking_code=tracking_code)

    if status is not None:
        valid_statuses = ['OK', 'FAILED', 'PENDING']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: {status}. Must be one of {valid_statuses}.")
        queryset = queryset.filter(status=status)

    if sort_by is not None:
        valid_sort_fields = ['amount', 'created_at', 'status']
        if sort_by not in valid_sort_fields:
            raise ValueError(f"Invalid sort_by field: {sort_by}. Must be one of {valid_sort_fields}.")
        sort_field = sort_by
        if order_by not in ['asc', 'desc']:
            raise ValueError("Order_by must be 'asc' or 'desc'.")
        if order_by == 'desc':
            sort_field = f'-{sort_field}'
        queryset = queryset.order_by(sort_field)

    return queryset