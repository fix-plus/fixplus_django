from django.utils import timezone

from fixplus.job.models import Job, ReferredJob
from fixplus.job.selectors.job import get_job
from fixplus.user.models import BaseUser
from fixplus.user.selectors.user import get_user


def create_referred_job_to_technician_by_admin(
        admin: BaseUser,
        job_id: str,
        technician_id: str,
):
    job = get_job(id=job_id)
    technician = get_user(id=technician_id)

    ReferredJob.objects.create(
        job=job,
        referred_by=admin,
        technician=technician,
        status='wait_determine_by_technician',
        referred_at=timezone.now(),
        deadline_determine_at=timezone.now() + timezone.timedelta(hours=24)
    )
