from django.urls import path

from src.parametric.apis.admin.brand import CreateBrandNameParametricApi, BrandNameParametricDetailApi
from src.parametric.apis.admin.device import CreateDeviceTypeParametricApi, DeviceTypeParametricDetailApi
from src.parametric.apis.admin.timing_setting import UpdateTimingSettingParametricApi
from src.parametric.apis.admin.warranty_period import CreateWarrantyPeriodParametricApi, \
    WarrantyPeriodParametricDetailApi
from src.parametric.apis.shared.brand import GetBrandNameParametricApi
from src.parametric.apis.shared.device import GetDeviceTypeParametricApi
from src.parametric.apis.shared.timing_setting import GetTimingSettingParametricApi
from src.parametric.apis.shared.warranty_period import GetWarrantyPeriodParametricApi

urlpatterns = [
    path('brand/create/', CreateBrandNameParametricApi.as_view(), name='create-brand'),
    path('brands/', GetBrandNameParametricApi.as_view(), name='brand-list'),
    path('brands/<uuid:pk>/', BrandNameParametricDetailApi.as_view(), name='brand-detail'),

    path('device-type/create/', CreateDeviceTypeParametricApi.as_view(), name='create-device-type'),
    path('device-types/', GetDeviceTypeParametricApi.as_view(), name='device-type-list'),
    path('device-types/<uuid:pk>/', DeviceTypeParametricDetailApi.as_view(), name='device-type-detail'),

    path('timing-settings/update/', UpdateTimingSettingParametricApi.as_view(), name='timing-setting-create'),
    path('timing-settings/', GetTimingSettingParametricApi.as_view(), name='timing-setting-list'),

    path('warranty-period/create/', CreateWarrantyPeriodParametricApi.as_view(), name='create-brand'),
    path('warranty-period/', GetWarrantyPeriodParametricApi.as_view(), name='brand-list'),
    path('warranty-period/<uuid:pk>/', WarrantyPeriodParametricDetailApi.as_view(), name='brand-detail'),
]