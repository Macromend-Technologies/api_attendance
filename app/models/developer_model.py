from django.db import models
from django.contrib.auth.hashers import make_password
from app.models.base_model import BaseModel


class Developer(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    is_super = models.BooleanField(default=True) 
    password = models.CharField(max_length=128) 

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
