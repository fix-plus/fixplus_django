from django.contrib import admin
from unfold.contrib.filters.admin import FieldTextFilter

from unfold.admin import ModelAdmin

from src.geo.models import Address


@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display = [
        "user",
        "customer",
        "address",
        "created_at",
    ]

    list_filter_submit = True