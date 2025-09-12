from app.models.base_model import BaseModel
from django.db import models


class AccessTypes(BaseModel):
    actions = models.CharField(max_length=60,null=False,blank=False,unique=True)
    param = models.CharField(max_length=60,null=False,blank=False,unique=True)
    
    def __str__(self):
        return  f"Param;{self.param}-{self.actions}"

class Roles(BaseModel):
    name = models.CharField(max_length=23,null=False,blank=False,unique=True)
    access = models.ManyToManyField( AccessTypes,related_name="role_access",blank=True)
    password=models 
    def __str__(self):
        return self.name



