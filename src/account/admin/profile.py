from django.contrib import admin
from django.utils.html import format_html
from unfold.contrib.filters.admin import FieldTextFilter

from unfold.admin import ModelAdmin

from src.account.models import Profile


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = [
        "display_avatar",
        "user",
        "full_name",
        "national_code",
    ]

    list_filter_submit = True
    list_filter = [
        ("full_name", FieldTextFilter),
        ("national_code", FieldTextFilter),
    ]

    def display_avatar(self, obj):
        """Return HTML for displaying the avatar."""
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />',
                obj.avatar.url
            )

        return "No Image"

    display_avatar.short_description = "Avatar"