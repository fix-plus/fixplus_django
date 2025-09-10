from django.urls import path

from src.parametric.apis.admin.brand import CreateBrandNameParametricApi, BrandNameParametricDetailApi
from src.parametric.apis.admin.device import CreateDeviceTypeParametricApi, DeviceTypeParametricDetailApi
from src.parametric.apis.admin.timing_setting import UpdateTimingSettingParametricApi
from src.parametric.apis.shared.brand import GetBrandNameParametricApi
from src.parametric.apis.shared.device import GetDeviceTypeParametricApi
from src.parametric.apis.shared.timing_setting import GetTimingSettingParametricApi
from src.parametric.apis.shared.warranty_period import GetWarrantyPeriodParametricApi

urlpatterns = [
    path('brands/', GetBrandNameParametricApi.as_view(), name='brand-list'),

    path('device-types/', GetDeviceTypeParametricApi.as_view(), name='device-type-list'),

    path('timing-settings/', GetTimingSettingParametricApi.as_view(), name='timing-setting-list'),

    path('warranty-period/', GetWarrantyPeriodParametricApi.as_view(), name='warranty-period-list'),
]