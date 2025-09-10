from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from src.common.models import BaseModel


class TimeUnitChoices(models.TextChoices):
    DAY = 'DAY', _('روز')
    MONTH = 'MONTH', _('ماه')
    YEAR = 'YEAR', _('سال')


class WarrantyPeriod(BaseModel):
    time_unit = models.CharField(max_length=10, choices=TimeUnitChoices.choices, default=TimeUnitChoices.MONTH)
    duration = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    duration_in_days = models.PositiveIntegerField(
        editable=False,
        verbose_name=_('مدت زمان به روز')
    )

    class Meta:
        ordering = ['duration_in_days']
        verbose_name = _('دوره گارانتی')
        verbose_name_plural = _('دوره‌های گارانتی')

    def __str__(self):
        return f"{self.duration}-{self.time_unit}"

    def calculate_duration_in_days(self):
        """Calculate duration in days."""
        if self.time_unit == TimeUnitChoices.DAY:
            return self.duration
        elif self.time_unit == TimeUnitChoices.MONTH:
            return self.duration * 30  # Assuming 1 month = 30 days
        elif self.time_unit == TimeUnitChoices.YEAR:
            return self.duration * 365  # Assuming 1 year = 365 days
        return 0

    def save(self, *args, **kwargs):
        """Override save to calculate duration_in_days before saving."""
        self.duration_in_days = self.calculate_duration_in_days()
        super().save(*args, **kwargs)