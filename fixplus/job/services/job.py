from fixplus.customer.selectors.selectors import get_customer
from fixplus.customer.services.services import create_customer_phone_number, create_customer
from fixplus.job.models import Job, ReferredJob
from fixplus.user.models import BaseUser


def create_job(*, added_by: BaseUser, customer_data=None, devices_data=None):
    customer = None

    if customer_data:
        customer_id = customer_data.get('customer_id')

        if customer_id:
            customer = get_customer(id=customer_id)
        else:
            customer = create_customer(
                added_by=added_by,
                full_name=customer_data.get('full_name'),
                gender=customer_data.get('gender')
            )

        phone_numbers = customer_data.get('phone_numbers')
        if phone_numbers:
            for index, number in enumerate(phone_numbers):
                create_customer_phone_number(customer=customer, number=number, is_default=(index == 0))

    if devices_data:
        job_instances = []
        for device in devices_data:
            job = Job(customer=customer)
            for key, value in device.items():
                setattr(job, key, value)

            job.status = 'in_assign_queue'
            job.save()
            job_instances.append(job)

        return job_instances

    return None