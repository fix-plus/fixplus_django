from django.contrib import admin
from unfold.contrib.filters.admin import FieldTextFilter

from unfold.admin import ModelAdmin

from src.service.models import Service


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = [
        "customer",
        "status",
    ]
    list_select_related = ["customer"]

    list_filter_submit = True
    list_filter = [
        ("customer__full_name", FieldTextFilter),
    ]