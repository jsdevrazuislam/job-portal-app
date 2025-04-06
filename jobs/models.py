from django.db import models
from ckeditor.fields import RichTextField
from authentication.models import CustomUser

# Create your models here.
class PostJobModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_profile',  null=True, blank=True)
    title = models.CharField(max_length=255, blank=False,  null=False)
    location = models.CharField(max_length=255,  blank=False,  null=False)
    type = models.CharField(max_length=20,  blank=False,  null=False)
    workMode = models.CharField(max_length=20,  blank=False,  null=False)
    salary = models.CharField(max_length=100,  blank=False,  null=False)
    experience = models.CharField(max_length=100,  blank=False,  null=False)
    education = models.CharField(max_length=100,  blank=False,  null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()
    body = RichTextField()

    def __str__(self):
        return f"{self.user.company_name} - {self.title}"