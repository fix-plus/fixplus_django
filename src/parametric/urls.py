from django.urls import path
from src.parametric.apis.apis import (
    BrandNameParametricApi, BrandNameParametricDetailApi,
    DeviceTypeParametricApi, DeviceTypeParametricDetailApi, TimingSettingParametricApi,
)


urlpatterns = [
    path('brands/', BrandNameParametricApi.as_view(), name='brand-list-create'),
    path('brands/<uuid:pk>/', BrandNameParametricDetailApi.as_view(), name='brand-detail'),
    path('device-types/', DeviceTypeParametricApi.as_view(), name='device-type-list-create'),
    path('device-types/<uuid:pk>/', DeviceTypeParametricDetailApi.as_view(), name='device-type-detail'),
    path('timing-settings/', TimingSettingParametricApi.as_view(), name='timing-setting-list-create'),
]