from app.models.base_model import BaseModel
from django.db import models

#  leave_request,permission_access

class AccessItems(BaseModel):
    param = models.CharField(max_length=60,null=False,blank=False,unique=True)
    def __str__(self):
        return  f"Items:{self.param}"
    
    #  Leave , Holiday & Permission 
class Actions(BaseModel):
    name = models.CharField(max_length=60,null=False,blank=False,unique=True) 
    def __str__(self):
        return  f"{self.name}"
    

    
 
    
class Designation(BaseModel):
    name = models.CharField(max_length=40,null=False,blank=False,unique=True)
    def __str__(self):
        return  f"{self.name}"
    
class Roles(BaseModel):
    name = models.CharField(max_length=23,null=False,blank=False,unique=True)
    def __str__(self):
        return self.name
    
    
 
class Access(BaseModel):
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, related_name="roles",null=True)
    action = models.ForeignKey(Actions, on_delete=models.CASCADE, related_name="actions",null=True)
    param = models.ManyToManyField(AccessItems,related_name="AccessItems",blank=True)  
    def __str__(self):
        return  f"Role-{self.role} Action:{self.action},Perm :{self.param} "



