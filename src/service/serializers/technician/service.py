import re

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from src.account.serializers.shared.profile import OutPutProfileSerializer
from src.customer.serializers.customer import OutPutCustomerSerializer
from src.financial.serializers.shared.customer_invoice import OutPutCustomerInvoiceSerializer
from src.geo.serializers.address import OutPutAddressSerializer
from src.parametric.serializers.brand import OutPutBrandNameParametricSerializer
from src.parametric.serializers.device import OutPutDeviceTypeParametricSerializer
from src.payment.serializers.customer_payment import OutputCustomerPaymentSerializer
from src.service.models import Service, ServiceHistory
from src.service.serializers.shared.completed_service_item import OutPutCompletedServiceItemSerializer


class OutPutTechnicianServiceDetailSerializer(serializers.ModelSerializer):
    customer = OutPutCustomerSerializer()
    brand = OutPutBrandNameParametricSerializer()
    device_type = OutPutDeviceTypeParametricSerializer()
    address = OutPutAddressSerializer()
    technician = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    assigned_by = serializers.SerializerMethodField()
    customer_invoice = serializers.SerializerMethodField()
    customer_payment = serializers.SerializerMethodField()
    invoice_deduction = serializers.SerializerMethodField()
    final_calculation = serializers.SerializerMethodField()
    assigned_at = serializers.SerializerMethodField()
    accepted_at = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        user = request.user

        # BaseFields
        base_fields = ['id',
                       'device_type',
                       'brand',
                       'description_for_technician',
                       'customer_description',
                       'address',
                       'status',
                       'customer',
                       'customer_invoice',
                       'customer_payment',
                       'invoice_deduction',
                       'other_invoice_deduction_description',
                       'final_calculation',
                       'assigned_by',
                       'assigned_at',
                       'deadline_accepting_at',
                       'estimate_arrival_at',
                       'accepted_at'
        ]

        if user.has_super_admin_or_admin():
            allowed_fields = base_fields + [
                "technician", "created_by", "created_at",
            ]
        else:  # Technician User
            allowed_fields = base_fields

        # Execute Final Fields
        for field_name in list(self.fields.keys()):
            if field_name not in allowed_fields:
                self.fields.pop(field_name)

    def get_technician(self, obj):
        request = self.context.get('request')
        try:
            return OutPutProfileSerializer(obj.technician.profile, user_type='public', context={'request':request}).data
        except:
            return None

    def get_created_by(self, obj):
        request = self.context.get('request')
        try:
            return OutPutProfileSerializer(obj.created_by.profile, user_type='public', context={'request':request}).data
        except:
            return None

    def get_assigned_by(self, obj):
        request = self.context.get('request')
        try:
            queryset = obj.histories.filter(new_status=Service.Status.ASSIGNED).latest('created_at').created_by
            return OutPutProfileSerializer(queryset.profile, user_type='public', context={'request':request}).data
        except ServiceHistory.DoesNotExist:
            return None

    def get_assigned_at(self, obj):
        try:
            queryset = obj.histories.filter(new_status=Service.Status.ASSIGNED).latest('created_at').created_at
            return queryset
        except ServiceHistory.DoesNotExist:
            return None

    def get_accepted_at(self, obj):
        try:
            queryset = obj.histories.filter(new_status=Service.Status.ACCEPTED, created_by=obj.technician).latest('created_at').created_at
            return queryset
        except ServiceHistory.DoesNotExist:
            return None

    def get_customer_invoice(self, obj):
        request = self.context.get('request')
        completed_service_items = obj.completed_service_items
        customer_invoice_response = OutPutCustomerInvoiceSerializer(obj.customer_invoice, context={'request': request}).data

        return {
            "completed_service_items": OutPutCompletedServiceItemSerializer(completed_service_items, context={'request':request}, many=True).data,
            **customer_invoice_response,
        }

    def get_customer_payment(self, obj):
        queryset = obj.customer_payments.filter(technician=obj.technician).last()
        return OutputCustomerPaymentSerializer(queryset).data

    def get_invoice_deduction(self, obj):
        queryset = obj.invoice_deduction_items
        return OutPutCompletedServiceItemSerializer(queryset, many=True).data

    def get_final_calculation(self, obj):
        return {
            "total_customer_pay": obj.customer_invoice.get_payable_amount(),
            "total_deduction": obj.customer_invoice.get_total_invoice_deduction_amount(),
            "system_fee": obj.customer_invoice.get_system_fee(),
        }
