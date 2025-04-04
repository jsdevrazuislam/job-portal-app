from django.urls import path
from .views import dashboard_home, applications, saved, settings, profile
from jobs.views import post_job

urlpatterns = [
    path('', dashboard_home, name='dashboard'),
    path('applications/', applications, name='applications'),
    path('saved/', saved, name='saved'),
    path('settings/', settings, name='settings'),
    path('profile/', profile, name='profile'),
    path('post_job/', post_job, name='post_job'),
]
