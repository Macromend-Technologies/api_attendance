from django.db import models
 
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    AbstractUser,
    PermissionsMixin
 
)
from app.models.base_model import BaseModel
from django.utils import timezone
from app.models.role_model import Roles
 
class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")
        user = self.create_user(email, password, **extra_fields)     
        user.save(using=self._db)
        return user

 
class CustomUser(AbstractBaseUser, PermissionsMixin,BaseModel):
    name  = models.CharField(max_length=25,null=False,blank=False)
    email =models.EmailField(unique=True,null=False,max_length=50)
    mobile =models.IntegerField(unique=True,null=True ,blank=False)
    role = models.ForeignKey("app.Roles", on_delete=models.CASCADE, related_name="user_role",null=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    

