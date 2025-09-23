from django.contrib import admin
from unfold.contrib.filters.admin import FieldTextFilter

from unfold.admin import ModelAdmin

from src.service.models import CompletedServiceItem


@admin.register(CompletedServiceItem)
class CompletedServiceItemAdmin(ModelAdmin):
    list_display = [
        "service",
        "description",
        "cost",
        "quantity",
    ]