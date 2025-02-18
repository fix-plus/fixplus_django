from django.contrib import admin
from unfold.contrib.filters.admin import FieldTextFilter

from unfold.admin import ModelAdmin

from src.customer.models import CustomerContactNumber


@admin.register(CustomerContactNumber)
class CustomerContactNumberAdmin(ModelAdmin):
    list_display = [
        "full_name",
        "phone_type",
        "number",
    ]
    list_select_related = ["customer"]

    list_filter_submit = True
    list_filter = [
        ("customer__full_name", FieldTextFilter),
    ]

    def full_name(self, obj):
        return obj.customer.full_name
