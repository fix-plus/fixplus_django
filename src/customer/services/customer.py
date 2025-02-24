from src.customer.models import Customer


def create_customer(*args, **kwargs):
    customer = Customer.objects.create(*args, **kwargs)
    return customer
