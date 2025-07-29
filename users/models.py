from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from .helper import get_file_path
from .const import *

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password = None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    last_login = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name_plural = USER_TABLE_SHOW_NAME


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, blank=True)
    birth_day = models.DateField(null=True)
    bio = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to=get_file_path)
    
    def __str__(self):
        return f"Profile of {self.user.email}"
    
    class Meta:
        verbose_name_plural = PROFILE_TABLE_SHOW_NAME