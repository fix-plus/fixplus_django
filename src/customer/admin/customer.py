from django.contrib import admin
from unfold.contrib.filters.admin import FieldTextFilter

from unfold.admin import ModelAdmin

from src.customer.models import Customer


@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    list_display = [
        "gender",
        "full_name",
        "created_at",
    ]

    list_filter_submit = True
    list_filter = [
        ("full_name", FieldTextFilter),
    ]
