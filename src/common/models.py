import uuid

from django.db import models
from django.db.models.query import F, Q
from django.utils import timezone


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    created_by = models.ForeignKey(
        'authentication.user',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='%(class)s_created_by'
    )
    created_at = models.DateTimeField(
        db_index=True,
        default=timezone.now
    )
    updated_by = models.ForeignKey(
        'authentication.user',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='%(class)s_updated_by'
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        """Override the delete method to perform a soft delete."""
        for obj in self:
            obj.soft_delete()

    def soft_delete(self):
        """Perform a soft delete on the queryset."""
        for obj in self:
            obj.is_deleted = True
            obj.deleted_at = timezone.now()
            obj.save()

    def restore(self):
        """Restore all soft-deleted objects in the queryset."""
        for obj in self:
            obj.restore()

    def deleted_objects(self):
        """Return a queryset that includes only soft-deleted objects."""
        return self.filter(is_deleted=True)

    def active_objects(self):
        """Return a queryset that includes only non-deleted objects."""
        return self.filter(is_deleted=False)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        """Return the custom queryset that excludes soft-deleted objects by default."""
        return SoftDeleteQuerySet(self.model, using=self._db).active_objects()

    def all_objects(self):
        """Return a queryset that includes all objects, including soft-deleted ones."""
        return SoftDeleteQuerySet(self.model, using=self._db)

    def deleted_objects(self):
        """Return a queryset that includes only soft-deleted objects."""
        return self.get_queryset().deleted_objects()

    def active_objects(self):
        """Return a queryset that includes only non-deleted objects."""
        return self.get_queryset().active_objects()


class SoftDeleteBaseModel(models.Model):
    is_deleted = models.BooleanField(
        default=False,
        editable=False
    )
    deleted_by = models.ForeignKey(
        'authentication.user',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='%(class)s_deleted_by'
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False
    )

    objects = SoftDeleteManager()  # Use the custom manager

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Override the delete method to perform a soft delete."""
        self.soft_delete()

    def soft_delete(self):
        """Perform a soft delete on the instance."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """Restore the soft-deleted object."""
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    @classmethod
    def clear(cls):
        """Permanently delete all soft-deleted objects."""
        cls.objects.deleted_objects().delete()  # This will permanently delete soft-deleted objects
