from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, CompanyProfile


@receiver(post_save, sender=CustomUser)
def create_company_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'employer':
        CompanyProfile.objects.create(user=instance, name=instance.company_name)

