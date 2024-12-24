from django.contrib import admin

from fixplus.customer.models import CustomerPhoneNumber, Customer

admin.site.register(CustomerPhoneNumber)
admin.site.register(Customer)
