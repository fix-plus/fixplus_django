from django.contrib.auth.models import Permission, Group
from django.utils.translation import gettext_lazy as _

from src.common.custom_exception import CustomAPIException
from src.authentication.models import User


def assign_permissions_to_group(group: Group, permission_codenames: list):
    permissions = Permission.objects.filter(codename__in=permission_codenames)
    if not permissions.exists():
        raise CustomAPIException(_("One or more permissions do not exist."))
    group.permissions.add(*permissions)
    group.save()


def remove_permissions_from_group(group: Group, permission_codenames: list):
    permissions = Permission.objects.filter(codename__in=permission_codenames)
    if not permissions.exists():
        raise CustomAPIException(_("One or more permissions do not exist."))
    group.permissions.remove(*permissions)
    group.save()


def assign_permissions_to_user(user: User, permission_codenames: list):
    permissions = Permission.objects.filter(codename__in=permission_codenames)
    if not permissions.exists():
        raise CustomAPIException(_("One or more permissions do not exist."))
    user.user_permissions.add(*permissions)
    user.save()


def remove_permissions_from_user(user: User, permission_codenames: list):
    permissions = Permission.objects.filter(codename__in=permission_codenames)
    if not permissions.exists():
        raise CustomAPIException(_("One or more permissions do not exist."))
    user.user_permissions.remove(*permissions)
    user.save()
