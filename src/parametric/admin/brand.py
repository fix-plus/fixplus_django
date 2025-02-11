from django.contrib import admin
from unfold.contrib.filters.admin import FieldTextFilter

from unfold.admin import ModelAdmin

from src.parametric.models import Brand


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = [
        "title",
        "fa_title",
        "description",
        "fa_description",
    ]