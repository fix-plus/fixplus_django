from django.contrib import admin
from unfold.contrib.filters.admin import FieldTextFilter

from unfold.admin import ModelAdmin

from src.payment.models import CustomerPayment


@admin.register(CustomerPayment)
class CustomerPaymentAdmin(ModelAdmin):
    list_display = [
        "service",
        "technician",
        "cash_amount",
        "card_to_card_amount",
        "cheque_amount",
        "online_amount",
    ]