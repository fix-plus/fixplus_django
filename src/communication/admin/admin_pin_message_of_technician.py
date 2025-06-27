from django.contrib import admin
from unfold.contrib.filters.admin import FieldTextFilter

from unfold.admin import ModelAdmin

from src.communication.models import AdminPinMessageOfTechnician


@admin.register(AdminPinMessageOfTechnician)
class AdminPinMessageOfTechnicianAdmin(ModelAdmin):
    list_display = [
        "user",
        "title",
        "created_at",
    ]
    list_select_related = ["user"]

    list_filter_submit = True
