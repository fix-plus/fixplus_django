from django.urls import path

from src.media.apis import UploadCenterApi


urlpatterns = [
    path('upload/', UploadCenterApi.as_view(),name="media-center"),
]