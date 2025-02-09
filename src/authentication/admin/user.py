from django.contrib import admin
from unfold.contrib.filters.admin import FieldTextFilter

from src.authentication.models import User
from unfold.admin import ModelAdmin


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = [
        "mobile",
        "is_verified_mobile",
        "last_online",
    ]

    list_filter_submit = True
    list_filter = [
        ("mobile", FieldTextFilter),
    ]