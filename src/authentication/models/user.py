import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.auth.models import UserManager as BUM
from django.contrib.auth.models import PermissionsMixin
from django.db.models import Q
from django.utils import timezone


class UserManager(BUM):
    def create_user(self,
                    mobile,
                    is_active=True,
                    is_admin=False,
                    password=None,
                    ):
        user = self.model(
            mobile=mobile,
            is_active=is_active,
            is_admin=is_admin,
        )
        # Assign identity_code before saving
        user.assign_identity_code()

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, mobile, password=None):
        from src.account.services.group import assign_groups_to_user

        user = self.create_user(
            mobile=mobile,
            is_active=True,
            is_admin=True,
            password=password,
        )
        # Assign identity_code before saving
        user.assign_identity_code()

        user.is_superuser = True
        user.is_verified_mobile = True
        user.save(using=self._db)

        # Explicitly assign all permissions
        all_permissions = Permission.objects.all()
        user.user_permissions.set(all_permissions)

        # Assign to super_user group
        assign_groups_to_user(user, ['SUPER_ADMIN'])

        return user


class User(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    identity_code = models.IntegerField(unique=True, null=True, blank=True)
    username = None
    mobile = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        default=True
    )
    is_verified_mobile = models.BooleanField(
        default=False
    )
    is_admin = models.BooleanField(
        default=False
    )
    last_online = models.DateTimeField(
        null=True,
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.mobile

    class Meta:
        permissions = [
            ("change_another", "Can change another account"),
        ]
        verbose_name = "User "

    def assign_identity_code(self):
        """Assign a unique identity_code to the user."""
        if not self.identity_code:
            last_user = User.objects.filter(identity_code__isnull=False).order_by('identity_code').last()
            self.identity_code = last_user.identity_code + 1 if last_user and last_user.identity_code else 1011

    def is_staff(self):
        return self.is_admin

    def get_tokens(self):
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def save(self, *args, **kwargs):
        # Assign identity_code before saving
        self.assign_identity_code()
        # Save user and create profile
        super().save(*args, **kwargs)
        from src.account.models import Profile
        Profile.objects.get_or_create(user=self)

    def update_last_online(self):
        self.last_online = timezone.now()
        self.save(update_fields=['last_online'])

    def has_super_admin_or_admin(self):
        return self.groups.filter(Q(name='SUPER_ADMIN') | Q(name='ADMIN')).exists()

    def has_super_admin(self):
        return self.groups.filter(name='SUPER_ADMIN').exists()

    def has_admin(self):
        return self.groups.filter(name='ADMIN').exists()

    def has_technician(self):
        return self.groups.filter(name='TECHNICIAN').exists()

    def get_role(self):
        if self.has_super_admin():
            return "SUPER_ADMIN"
        elif self.has_admin():
            return "ADMIN"
        elif self.has_technician():
            return "TECHNICIAN"
        else:
            return "USER"