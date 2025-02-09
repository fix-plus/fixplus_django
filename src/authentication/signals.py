from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission

from src.authentication.models import User


@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    if sender.name != 'src.authentication':
        return

    groups = {
        'super_admin': [],
        'admin': [],
        'technician': [],
    }

    for group_name, permissions in groups.items():
        group, created = Group.objects.get_or_create(name=group_name)
        if group_name == 'super_admin':
            # Assign all permissions to super_admin
            group.permissions.set(Permission.objects.all())
        else:
            # Assign specific permissions
            perms = Permission.objects.filter(codename__in=permissions)
            group.permissions.set(perms)
        group.save()


@receiver(post_migrate)  # TODO: Remove in production
def create_superuser(sender, **kwargs):
    """Create a superuser after migrations if it does not exist."""

    if sender.name == "src.authentication":
        if not User.objects.filter(mobile='admin@admin.com').exists():
            User.objects.create_superuser(
                mobile='admin@admin.com',
                password='1234@1234',
            )
            print("Superuser created with username: admin")