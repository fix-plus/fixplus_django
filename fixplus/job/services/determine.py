from django.utils import timezone
from rest_framework.fields import DateTimeField
from django.utils.translation import gettext_lazy as _

from fixplus.job.selectors.referred import get_referred_job
from fixplus.user.models import BaseUser


def update_determine_referred_job_with_technician(
        technician: BaseUser,
        referred_job_id: str,
        status: str,
        estimated_arrival_at: DateTimeField | None = None,
        rejected_reason_by_technician: str | None = None,
):
    referred_job = get_referred_job(id=referred_job_id)
    job = referred_job.job

    if referred_job.technician != technician: raise Exception(_("You do not have access to do this."))
    if referred_job.status != 'wait_determine_by_technician': raise Exception(_("You do not have access to do this."))
    if status == 'rejected' and not rejected_reason_by_technician: raise Exception(_("You must enter the reason for rejection."))
    if timezone.now() > referred_job.deadline_determine_at:
        referred_job.objects.update(status='expired')
        raise Exception(_("You do not have access to do this."))

    referred_job.status = status
    referred_job.estimated_arrival_at = estimated_arrival_at
    referred_job.rejected_reason_by_technician = rejected_reason_by_technician


    referred_job.save()
