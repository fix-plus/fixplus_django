from django.contrib import admin
from unfold.contrib.filters.admin import FieldTextFilter

from unfold.admin import ModelAdmin

from src.service.models import ServiceHistory


@admin.register(ServiceHistory)
class ServiceHistoryAdmin(ModelAdmin):
    list_display = [
        "service",
        "previous_status",
        "new_status"
    ]
    list_select_related = ["service"]

    list_filter_submit = True
    list_filter = [
        ("service__customer__full_name", FieldTextFilter),
    ]