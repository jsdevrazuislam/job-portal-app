from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db import models
from django.contrib.auth import get_user_model

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
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, first_name, last_name, avatar=None, company_name="Own Company", password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('job-seeker', 'Job Seeker'),
        ('employer', 'Employer'),
        ('recruiter', 'Recruiter'),
        ('admin', 'Admin'),
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

User = get_user_model()

class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255, unique=True)
    stripe_customer_id = models.CharField(max_length=255)
    plan_name = models.CharField(max_length=100)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=255)
    invoice_url = models.URLField(null=True, blank=True)
    receipt_url = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=50, default='active')
    start_date = models.DateTimeField()
    next_billing_date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan_name}"

class CompanyProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='company_profile')
    name = models.CharField(max_length=255)
    industry = models.CharField(blank=True, null=True, max_length=255)
    company_size = models.CharField(blank=True, null=True, max_length=255)
    build_year = models.CharField(max_length=10, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='company_logo/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
