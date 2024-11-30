from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django_celery_results.admin import TaskResult, GroupResult
from django_celery_beat.models import (
    IntervalSchedule,
    CrontabSchedule,
    SolarSchedule,
    ClockedSchedule,
    PeriodicTask,
)

from .models.profile import Profile, MobileNumber, LandLineNumber


#Register your models here.
@admin.register(get_user_model())
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ('mobile', 'status', 'reason_for_rejected')
    list_filter = ('status',)
    search_fields = ('mobile',)

    def save_model(self, request, obj, form, change):
        if obj.status == 'rejected' and not obj.reason_for_rejected:
            raise ValueError("You must provide a reason when rejecting a user.")
        super().save_model(request, obj, form, change)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name')
    ordering = ('-created_at',)


admin.site.register(MobileNumber)
admin.site.register(LandLineNumber)


# UnRegister
admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(Group)