from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Permission
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from fixplus.common.models import BaseModel


class BaseUserManager(BUM):
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

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, mobile, password=None):
        from fixplus.user.services.group import assign_groups_to_user

        user = self.create_user(
            mobile=mobile,
            is_active=True,
            is_admin=True,
            password=password,
        )

        user.is_superuser = True
        user.is_staff = True
        user.status = 'registered'
        user.is_verified_mobile = True
        user.save(using=self._db)

        # Explicitly assign all permissions
        all_permissions = Permission.objects.all()
        user.user_permissions.set(all_permissions)

        # Assign to super_user group
        assign_groups_to_user(user, ['super_admin'])

        return user


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    mobile = models.CharField(max_length=20, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_verified_mobile = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    request_register_datetime = models.DateTimeField(blank=True, null=True)

    # New field to track last online time
    last_online = models.DateTimeField(null=True, blank=True)

    STATUS_CHOICES = [
        ('not_registered', 'Not Registered'),
        ('checking', 'Checking Identity'),
        ('registered', 'Registered'),
        ('rejected', 'Rejected'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_registered',
    )

    reason_for_rejected = models.TextField(
        blank=True,
        null=True,
        help_text="Provide the reason for rejecting the user if the status is 'Rejected'."
    )

    objects = BaseUserManager()

    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.mobile

    class Meta:
        permissions = [
            ("change_another", "Can change another user"),
        ]
        verbose_name = "User "

    def get_tokens(self):
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def save(self, *args, **kwargs):
        # If status is 'rejected', ensure 'reason_for_rejected' is provided
        if self.status == 'rejected' and not self.reason_for_rejected:
            raise ValueError("You must provide a reason when rejecting a user.")

        # Call the parent class save method
        super().save(*args, **kwargs)

        # Ensure a Profile exists for this user
        from fixplus.user.models import Profile
        Profile.objects.get_or_create(user=self)

    def update_last_online(self):
        self.last_online = timezone.now()
        self.save(update_fields=['last_online'])