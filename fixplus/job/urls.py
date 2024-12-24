from django.urls import path

from fixplus.job.apis.job import JobListApi
from fixplus.job.apis.referred import ReferredJobToTechnicianListApi
from fixplus.job.apis.determine import DetermineReferredJobWithTechnicianApi
from fixplus.job.apis.technician_for_job import TechnicianForJobListApi

urlpatterns = [
    path('technician-for-job/', TechnicianForJobListApi.as_view(), name='technician-for-job'),
    path('referred-job/', ReferredJobToTechnicianListApi.as_view(), name='referred-job'),
    path('determine-referred-job/', DetermineReferredJobWithTechnicianApi.as_view(), name='determine-referred-job'),
    path('', JobListApi.as_view(), name='job-list'),
]
