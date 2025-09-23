from django.contrib import admin
from unfold.contrib.filters.admin import FieldTextFilter

from unfold.admin import ModelAdmin

from src.financial.models import CustomerInvoice


@admin.register(CustomerInvoice)
class CustomerInvoiceAdmin(ModelAdmin):
    list_display = [
        "service",
        "wage_cost",
    ]