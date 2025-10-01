from django.contrib import admin
from unfold.contrib.filters.admin import FieldTextFilter

from unfold.admin import ModelAdmin

from src.financial.models import InvoiceDeductionItem


@admin.register(InvoiceDeductionItem)
class InvoiceDeductionItemAdmin(ModelAdmin):
    list_display = [
        "service",
        "description",
        "quantity",
        "cost",
    ]