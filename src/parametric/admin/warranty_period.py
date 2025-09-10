from django.contrib import admin

from unfold.admin import ModelAdmin

from src.parametric.models import WarrantyPeriod


@admin.register(WarrantyPeriod)
class WarrantyPeriodAdmin(ModelAdmin):
    list_display = [
        "duration",
        "time_unit",
    ]