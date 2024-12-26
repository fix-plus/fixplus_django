from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from fixplus.job.models import Job, ReferredJob
from fixplus.job.selectors.job import get_job
from fixplus.parametric.selectors.selectors import get_timing_setting
from fixplus.user.models import BaseUser
from fixplus.user.selectors.user import get_user


def create_referred_job_to_technician_by_admin(
        admin: BaseUser,
        job_id: str,
        technician_id: str,
):
    job = get_job(id=job_id)
    technician = get_user(id=technician_id)
    timing_setting_db = get_timing_setting()

    if job.status != 'in_referred_queue' : raise Exception(_("This job has already been referred."))

    ReferredJob.objects.create(
        job=job,
        referred_by=admin,
        technician=technician,
        status='wait_determine_by_technician',
        referred_at=timezone.now(),
        deadline_determine_at=timezone.now() + timezone.timedelta(minutes=timing_setting_db.max_wait_determine_referred_job_by_tech_min)
    )
