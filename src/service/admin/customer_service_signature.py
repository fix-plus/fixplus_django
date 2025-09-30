from django.contrib import admin
from unfold.contrib.filters.admin import FieldTextFilter

from unfold.admin import ModelAdmin

from src.service.models import CustomerServiceSignature


@admin.register(CustomerServiceSignature)
class CustomerServiceSignatureAdmin(ModelAdmin):
    list_display = [
        "service",
    ]