from django.contrib import admin
from .models import CustomUser, CompanyProfile, UserSubscription
# Register your models here.
admin.site.register([CustomUser, CompanyProfile, UserSubscription])
