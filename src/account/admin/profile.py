from django.contrib import admin
from unfold.contrib.filters.admin import FieldTextFilter

from unfold.admin import ModelAdmin

from src.account.models import Profile


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = [
        "user",
        "full_name",
        "national_code",
    ]

    list_filter_submit = True
    list_filter = [
        ("full_name", FieldTextFilter),
        ("national_code", FieldTextFilter),
    ]