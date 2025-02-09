from django.db import models

from src.common.models import BaseModel


class TimingSetting(BaseModel):
    max_wait_referred_job_to_tech_min = models.PositiveIntegerField(default=30)
    # is_notify_after_expired_referred_job_to_tech = models.BooleanField(default=True)
    max_wait_determine_referred_job_by_tech_min = models.PositiveIntegerField(default=15)
    # is_notify_after_expired_determine_referred_job_by_tech = models.BooleanField(default=True)
    max_jobs_per_day_by_tech = models.PositiveIntegerField(default=3)
    max_processing_jobs_by_tech_hour = models.PositiveIntegerField(default=72)
    # is_notify_after_expired_processing_job_by_tech = models.BooleanField(default=True)
    # is_cancel_job_after_expired_processing_by_tech = models.BooleanField(default=False)
    max_wait_determine_follow_up_tag_hour = models.PositiveIntegerField(default=24)
    # is_notify_after_expired_determine_follow_up_tag = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Timing Settings"
        verbose_name_plural = "Timing Settings"

    def save(self, *args, **kwargs):
        if TimingSetting.objects.exists():
            TimingSetting.objects.get().delete()
            super().save(*args, **kwargs)
        super().save(*args, **kwargs)

    def __str__(self):
        return "Setting"