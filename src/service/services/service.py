from src.customer.models import CustomerContactNumber
from src.customer.selectors.customer import get_customer
from src.customer.services.customer import create_customer
from src.geo.models import Address
from src.service.models import Service
from src.parametric.models import DeviceType, Brand
from src.authentication.models import User


def create_job(
        *, created_by: User,
        customer_data=None,
        devices_data=None
):
    customer = None

    if customer_data:
        customer_id = customer_data.get('customer_id')

        if customer_id:
            customer = get_customer(id=customer_id)
        else:
            customer = create_customer(
                created_by=created_by,
                full_name=customer_data.get('full_name'),
                gender=customer_data.get('gender')
            )

        contact_numbers = customer_data.get('contact_numbers')
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

    if devices_data:
        service_instances = []
        for device in devices_data:
            service = Service(customer=customer)
            for key, value in device.items():
                if key == 'device_type' and value is not None:
                    service.device_type = DeviceType.objects.get(title=value)
                elif key == 'brand' and value is not None:
                    service.brand = Brand.objects.get(title=value)
                elif key == 'address' and value is not None:
                    query, is_created = Address.objects.get_or_create(
                        customer=customer,
                        address=value
                    )
                    service.address = query
                elif key == 'latitude' and value is not None:
                    if service.address is None:
                        query, is_created = Address.objects.get_or_create(
                            customer=customer,
                            latitude=value
                        )
                        service.address = query
                    else:
                        query = service.address
                        query.latitude = value
                        query.save()

                elif key == 'longitude' and value is not None:
                    if service.address is None:
                        query, is_created = Address.objects.get_or_create(
                            customer=customer,
                            longitude=value
                        )
                        service.address = query
                    else:
                        query = service.address
                        query.longitude = value
                        query.save()
                else:
                    setattr(service, key, value)

            service.status = Service.Status.WAITING
            service.created_by = created_by
            service.save()
            service_instances.append(service)

        return service_instances

    return None