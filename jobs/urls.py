from django.urls import path
from .views import view_jobs, job_details, post_job

urlpatterns = [
    path('', view_jobs, name='view_jobs'),
    path('<int:job_id>', job_details, name='job_details'),
    path('post-job/', post_job, name='post_job'),
]