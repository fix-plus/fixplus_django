from django.contrib import admin
from unfold.contrib.filters.admin import FieldTextFilter

from unfold.admin import ModelAdmin

from src.geo.models import UserLocationTracker


@admin.register(UserLocationTracker)
class UserLocationTrackerAdmin(ModelAdmin):
    list_display = [
        "mobile",
        "full_name",
        "created_at",
    ]
    list_select_related = ["user"]

    list_filter_submit = True
    list_filter = [
        ("user__mobile", FieldTextFilter),
        ("user__profile__national_code", FieldTextFilter),
        ("user__profile__full_name", FieldTextFilter),
    ]

    def mobile(self, obj):
        return obj.user.mobile

    def full_name(self, obj):
        return obj.user.profile.full_name