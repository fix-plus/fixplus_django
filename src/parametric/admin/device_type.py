from django.contrib import admin
from unfold.contrib.filters.admin import FieldTextFilter

from unfold.admin import ModelAdmin

from src.parametric.models import DeviceType


@admin.register(DeviceType)
class DeviceTypeAdmin(ModelAdmin):
    list_display = [
        "title",
        "fa_title",
    ]