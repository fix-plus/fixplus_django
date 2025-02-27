from django.db.models.signals import post_save
from django.dispatch import receiver

from src.account.models import UserRegistryRequest


@receiver(post_save, sender=UserRegistryRequest)
def create_technician_status(sender, instance, created, **kwargs):
    """
    Signal receiver to create a default active status for a technician when a user is created
    and assigned to the technician group.

    Args:
        sender (Model): The model class that sent the signal.
        instance (UserRegistryRequest): The instance of the model that triggered the signal.
        created (bool): A boolean indicating whether a new record was created.
        **kwargs: Additional keyword arguments.

    """
    if created:
        if instance.status == UserRegistryRequest.APPROVED and \
            instance.user.groups.filter(name='technician').exists() and \
            not instance.user.technician_statuses.exists():

            instance.user.technician_statuses.create(status='active')