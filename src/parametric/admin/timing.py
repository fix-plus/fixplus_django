from django.contrib import admin
from unfold.contrib.filters.admin import FieldTextFilter

from unfold.admin import ModelAdmin

from src.parametric.models import TimingSetting


@admin.register(TimingSetting)
class TimingSettingAdmin(ModelAdmin):
    pass