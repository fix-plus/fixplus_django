from django.urls import path

from fixplus.job.apis.job import JobListApi
from fixplus.job.apis.referred import ReferredJobToTechnicianListApi
from fixplus.job.apis.determine import DetermineReferredJobWithTechnicianApi

urlpatterns = [
    path('referred-job/', ReferredJobToTechnicianListApi.as_view(), name='referred-job'),
    path('determine-referred-job/', DetermineReferredJobWithTechnicianApi.as_view(), name='determine-referred-job'),
    path('', JobListApi.as_view(), name='job-list'),
]
