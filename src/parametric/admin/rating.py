from django.contrib import admin
from unfold.contrib.filters.admin import FieldTextFilter

from unfold.admin import ModelAdmin

from src.parametric.models import Rating


@admin.register(Rating)
class RatingAdmin(ModelAdmin):
    list_display = [
        "title",
        "description",
        "created_at",
    ]