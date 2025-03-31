from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, avatar=None, company_name="", password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not first_name or not last_name:
            raise ValueError("First name and Last name are required")

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, avatar=avatar, company_name=company_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, first_name, last_name, avatar=None, company_name="Own Company", password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('job-seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    ]
    username = None
    email = models.EmailField(unique=True, blank=False, null=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True) 
    role = models.CharField(max_length=20, choices=ROLES, default='job-seeker')
    company_name = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS = ["first_name", "last_name"]  

    def __str__(self):
        return self.email