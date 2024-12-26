from django.db import models

from fixplus.common.models import BaseModel
from fixplus.user.models import BaseUser


class BrandNameParametric(BaseModel):
    title = models.CharField(max_length=100, null=False)
    fa_title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True, blank=True,)
    fa_description = models.TextField(null=True, blank=True,)

    class Meta:
        pass

    def __str__(self):
        return f"{self.title}-{self.fa_title}"


class DeviceTypeParametric(BaseModel):
    title = models.CharField(max_length=100, null=False)
    fa_title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True, blank=True,)
    fa_description = models.TextField(null=True, blank=True,)

    class Meta:
        pass

    def __str__(self):
        return f"{self.title}-{self.fa_title}"


class TimingSettingParametric(BaseModel):
    max_wait_referred_job_to_tech_min = models.PositiveIntegerField(default=30)
    is_notify_after_expired_referred_job_to_tech = models.BooleanField(default=True)
    max_wait_determine_referred_job_by_tech_min = models.PositiveIntegerField(default=15)
    is_notify_after_expired_determine_referred_job_by_tech = models.BooleanField(default=True)
    max_jobs_per_day_by_tech = models.PositiveIntegerField(default=3)
    max_processing_jobs_by_tech_hour = models.PositiveIntegerField(default=72)
    is_notify_after_expired_processing_job_by_tech = models.BooleanField(default=True)
    is_cancel_job_after_expired_processing_by_tech = models.BooleanField(default=False)
    max_wait_determine_follow_up_tag_hour = models.PositiveIntegerField(default=24)
    is_notify_after_expired_determine_follow_up_tag = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Timing Settings"
        verbose_name_plural = "Timing Settings"

    def save(self, *args, **kwargs):
        if TimingSettingParametric.objects.exists():
            TimingSettingParametric.objects.get().delete()
            super().save(*args, **kwargs)
        super().save(*args, **kwargs)

    def __str__(self):
        return "Setting"
