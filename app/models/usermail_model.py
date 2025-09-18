from app.models.base_model import BaseModel
from django.db import models
from app.models.role_model import Designation, Roles

class CompanyUserMails(BaseModel):
    email =models.EmailField(unique=True,null=False,max_length=50)
    role = models.ForeignKey("app.Roles", on_delete=models.CASCADE, related_name="user_mails",null=True)
    designation = models.ManyToManyField( Designation,related_name="designations_mails",blank=True)  
    is_active =models.BooleanField(default=False)
 
    def __str__(self):
        return  f"{self.email}--{self.role.name}"