from django.db import transaction

from src.customer.models import Customer


from src.communication.models import CustomerPinMessage
from src.customer.models import CustomerContactNumber


def create_customer(
        **kwargs
):
    customer = Customer.objects.create(
        created_by=kwargs.get('created_by'),
        full_name=kwargs.get('full_name'),
        gender=kwargs.get('gender')
    )

    contact_numbers = kwargs.get('contact_numbers')
    if contact_numbers:
        for index, item in enumerate(contact_numbers):
            CustomerContactNumber.objects.get_or_create(
                customer=customer,
                number=item.get('number'),
                defaults={
                    'phone_type': item.get('phone_type'),
                    'is_primary': item.get('is_primary'),
                }
            )

    pin_message = kwargs.get('pin_message')
    if pin_message:
        CustomerPinMessage.objects.create(
            customer=customer,
            description=pin_message,
        )

    return customer


@transaction.atomic
def update_customer(
        instance: Customer,
        **kwargs
):

    for key, value in kwargs.items():
        if key == 'contact_numbers' and value:
            CustomerContactNumber.objects.filter(customer=instance).delete()
            for index, item in enumerate(value):
                CustomerContactNumber.objects.get_or_create(
                    customer=instance,
                    number=item.get('number'),
                    defaults={
                        'phone_type': item.get('phone_type'),
                        'is_primary': item.get('is_primary'),
                    }
                )

        elif key == 'pin_message' and value:
            CustomerPinMessage.objects.create(
                customer=instance,
                description=value,
            )

        elif value:
            setattr(instance, key, value)

    instance.save()
    return instance


def delete_customer(instance: Customer):
    instance.delete()
    return instance
