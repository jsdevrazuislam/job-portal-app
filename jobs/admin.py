from django.contrib import admin
from .models import PostJobModel
from authentication.models import JobApplication,Profession,Skill,UserProfile

# Register your models here.
admin.site.register([PostJobModel, JobApplication, Profession, Skill, UserProfile])
