from app.models.base_model import BaseModel
from django.db import models
from app.models.role_model import Designation, Roles

class CompanyUserMails(BaseModel):
    email =models.EmailField(unique=True,null=False,max_length=50)
    designation = models.ForeignKey("app.Designation", on_delete=models.CASCADE, related_name="user_designation",null=True)
    role = models.ManyToManyField("app.Roles" ,related_name="company_role",blank=True)  
    is_active =models.BooleanField(default=False)
 
    def __str__(self):
        return  f"{self.email}--{self.role.name}"