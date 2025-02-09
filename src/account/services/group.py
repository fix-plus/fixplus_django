from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from src.common.custom_exception import CustomAPIException
from src.authentication.models import User


def assign_groups_to_user(user: User, group_names: list):
    groups = Group.objects.filter(name__in=group_names)
    if not groups.exists():
        raise CustomAPIException(_("One or more groups do not exist."))
    user.groups.add(*groups)
    user.save()


def remove_groups_from_user(user: User, group_names: list):
    groups = Group.objects.filter(name__in=group_names)
    if not groups.exists():
        raise CustomAPIException(_("One or more groups do not exist."))
    user.groups.remove(*groups)
    user.save()
