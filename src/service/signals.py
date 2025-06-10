from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from src.service.models import Service, ServiceHistory


@receiver(post_save, sender=Service)
def log_service_save(sender, instance, created, **kwargs):
    """
    Logs creation or update events for a Service instance, with optional custom remarks.
    """
    # Check for custom remark, fall back to default if not provided
    custom_remark = getattr(instance, "_custom_remark", None)

    if created:
        # Log creation event with custom or default remark
        remark = custom_remark if custom_remark else "Service created."
        ServiceHistory.objects.create(
            service=instance,
            event_type=ServiceHistory.EventType.CREATE,
            new_status=instance.status,
            created_by=instance.created_by,
            remarks=remark,
        )
    else:
        try:
            latest_history = ServiceHistory.objects.filter(service=instance).latest("created_at")
            if latest_history.new_status != instance.status:
                remark = custom_remark if custom_remark else "Service status updated."
                ServiceHistory.objects.create(
                    service=instance,
                    event_type=ServiceHistory.EventType.UPDATE,
                    previous_status=latest_history.new_status,
                    new_status=instance.status,
                    created_by=instance.updated_by,
                    remarks=remark,
                )
        except sender.DoesNotExist:
            pass  # Safety net

    # Clean up the temporary attribute if it exists
    if hasattr(instance, "_custom_remark"):
        del instance._custom_remark


@receiver(pre_delete, sender=Service)
def log_service_delete(sender, instance, **kwargs):
    """
    Logs delete events for a Service instance, with optional custom remarks.
    """
    # Check for custom remark, fall back to default if not provided
    custom_remark = getattr(instance, "_custom_remark", None)
    remark = custom_remark if custom_remark else "Service deleted."

    ServiceHistory.objects.create(
        service=instance,
        event_type=ServiceHistory.EventType.DELETE,
        previous_status=instance.status,
        created_by=instance.updated_by or instance.created_by,  # Fallback to created_by if no updated_by
        remarks=remark,
    )
    # Clean up the temporary attribute if it exists
    if hasattr(instance, "_custom_remark"):
        del instance._custom_remark