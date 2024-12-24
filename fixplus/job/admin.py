from django.contrib import admin

from fixplus.job.models import Job, ReferredJob

admin.site.register(Job)
admin.site.register(ReferredJob)
