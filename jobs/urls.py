from django.urls import path
from .views import view_jobs, job_details

urlpatterns = [
    path('', view_jobs, name='view_jobs'),
    path('<int:job_id>', job_details, name='job_details'),
]