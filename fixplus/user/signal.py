# users/signals.py

from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver


@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    if sender.name != 'fixplus.user':
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
