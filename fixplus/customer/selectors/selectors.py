from django.db.models import Subquery

from fixplus.customer.models import Customer, CustomerPhoneNumber


def get_customer_phone_numbers(customer: Customer) -> CustomerPhoneNumber:
    return CustomerPhoneNumber.objects.filter(customer=customer)


def get_customer(*, id: str) -> CustomerPhoneNumber:
    return CustomerPhoneNumber.objects.filter(id=id)


def search_customer_list(
    phone: str = None,
    full_name: str | None = None,
    sort_by: str = 'created_at',
    order: str = 'desc'  # Default to descending order
) -> Customer :

    queryset = Customer.objects.all()

    # Filter by mobile if provided
    if phone:
        mobile_queryset = CustomerPhoneNumber.objects.filter(number__startswith=phone)
        customer_ids = mobile_queryset.values_list('customer_id', flat=True).distinct()
        queryset = Customer.objects.filter(id__in=customer_ids)
        queryset = queryset.annotate(
            searched_phone_number=Subquery(mobile_queryset.values('number')[:1])
        )

    # Join with Profile to filter by full_name if provided
    if full_name:
        queryset = queryset.filter(full_name__istartswith=full_name)

    # Determine the order direction
    order_prefix = '-' if order == 'desc' else ''

    # Sort the results if sort_by is provided
    if sort_by:
        if sort_by in ['created_at', 'updated_at',]:
            queryset = queryset.order_by(f"{order_prefix}{sort_by}")
        else:
            raise ValueError("Invalid sort_by value. Must be one of: 'created_at', 'last_online',.")

    return queryset