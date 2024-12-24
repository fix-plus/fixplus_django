from django.db.models.signals import post_save
from django.dispatch import receiver

from fixplus.job.models import ReferredJob


@receiver(post_save, sender=ReferredJob)
def update_job_status(sender, instance, created, **kwargs):
    # Check the status of the ReferredJob instance
    if instance.status == 'accept_by_technician':
        instance.job.status = 'in_processing'
    elif instance.status == 'rejected_by_technician':
        instance.job.status = 'rejected_by_technician'

    # Save the updated Job status
    instance.job.save()