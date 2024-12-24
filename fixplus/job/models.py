from django.db import models

from fixplus.common.models import SoftDeleteBaseModel
from fixplus.customer.models import Customer
from fixplus.user.models import BaseUser


class Job(SoftDeleteBaseModel):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('in_assign_queue', 'In Assign Queue'),
        ('wait_assign_by_technician', 'Wait Assign By Technician'),
        ('in_processing', 'In Processing'),
        ('canceled', 'Canceled'),
        ('rejected_by_technician', 'Rejected By Technician'),
        ('done', 'Done'),
    ]
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='draft', )
    customer = models.ForeignKey(Customer, null=False, blank=False, related_name="job_customer", on_delete=models.CASCADE)
    device_type = models.CharField(max_length=100, blank=False, null=False)
    brand_name = models.CharField(max_length=100, blank=False, null=False)
    customer_description = models.TextField(blank=True, null=True)
    description_for_technician = models.TextField(blank=True, null=True)
    address = models.TextField(blank=False, null=False)

    class Meta:
        pass

    def __str__(self):
        return f"{self.customer.full_name} : {self.brand_name}-{self.device_type}"


class ReferredJob(SoftDeleteBaseModel):
    STATUS_CHOICES = [
        ('wait_determine_by_technician', 'Wait Determine By Technician'),
        ('in_processing', 'In Processing'),
        ('canceled_by_admin', 'Canceled By Admin'),
        ('changed_technician_by_admin', 'Changed Technician By Admin'),
        ('rejected_by_technician', 'Rejected By Technician'),
        ('expired', 'Expired'),
        ('done', 'Done'),
    ]
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='wait_determine_by_technician', )
    job = models.ForeignKey(Job, null=False, blank=False, on_delete=models.CASCADE)
    technician = models.ForeignKey(BaseUser, null=False, blank=False, on_delete=models.CASCADE, related_name="referred_job_technician")
    referred_by = models.ForeignKey(BaseUser, null=False, blank=False, on_delete=models.CASCADE, related_name="referred_job_referred_by")  # Admin Users
    updated_by = models.ForeignKey(BaseUser, null=True, blank=True, on_delete=models.CASCADE, related_name="referred_job_updated_by")  # Admin Users
    referred_at = models.DateTimeField(null=True, blank=True)  # Referred by admin to technician at
    deadline_determine_at = models.DateTimeField(null=True, blank=True)
    estimated_arrival_at = models.DateTimeField(null=True, blank=True)
    determined_by_technician_at = models.DateTimeField(null=True, blank=True)
    rejected_reason_by_technician = models.TextField(blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return f"{self.job.brand_name}-{self.job.device_type}"
