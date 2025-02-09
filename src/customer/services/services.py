from src.customer.models import Customer, CustomerPhoneNumber


def create_customer_phone_number(customer: Customer, *args, **kwargs):
    customer_phone_number, created = CustomerPhoneNumber.objects.get_or_create(
        customer=customer,
        *args,
        **kwargs,
    )
    return customer_phone_number


def create_customer(*args, **kwargs):
    customer = Customer.objects.create(*args, **kwargs)
    return customer
