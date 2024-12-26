from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django_celery_results.admin import TaskResult, GroupResult
from django_celery_beat.models import (
    IntervalSchedule,
    CrontabSchedule,
    SolarSchedule,
    ClockedSchedule,
    PeriodicTask,
)

from .models import BaseUser
from .models.profile import Profile, MobileNumber, LandLineNumber
from .models.skill import TechnicianSkill


# Customize Group admin to manage permissions
class CustomGroupAdmin(GroupAdmin):
    filter_horizontal = ['permissions']


admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)


# Register BaseUser model
@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ['mobile', 'is_active', 'is_verified_mobile', 'status']
    list_filter = ['is_active', 'is_verified_mobile', 'status']
    search_fields = ['mobile']
    # ordering = ['-created_at']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name')
    ordering = ('-created_at',)


admin.site.register(MobileNumber)
admin.site.register(LandLineNumber)
admin.site.register(TechnicianSkill)


# UnRegister
admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)