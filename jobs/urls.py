from django.urls import path
from .views import view_jobs

urlpatterns = [
    path('', view_jobs, name='view_jobs')
]