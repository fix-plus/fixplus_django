from django.contrib import admin

from fixplus.parametric.models import BrandNameParametric, DeviceTypeParametric, TimingSettingParametric


admin.site.register(BrandNameParametric)
admin.site.register(DeviceTypeParametric)
admin.site.register(TimingSettingParametric)