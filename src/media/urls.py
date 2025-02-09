from django.urls import path

from src.media.apis import UploadCenterApi


urlpatterns = [
    path('', UploadCenterApi.as_view(),name="media-center"),
]