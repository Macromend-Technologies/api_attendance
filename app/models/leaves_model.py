from django.db import models
from app.models.base_model import BaseModel
from app.permission import CustomUser
 
 
class LeaveType(BaseModel):
    name= models.CharField(max_length=30,null=False,unique=True)
    def __str__(self):
        return self.name
 
class Leaves(BaseModel):
    DATE_RANGE_STATUS = [("single", "Single"), ("multiple", "Multiple") ]
    STATUS = [("pending", "Pending"), ("approve", "Approve"),("decline", "Decline")]
    REVIWER_STATUS = [("pending", "Pending"), ("approve", "Approve"),("decline", "Decline")]
    
    user =models.ForeignKey("app.CustomUser", on_delete=models.CASCADE, related_name="user_leave",null=True)
    date_range =models.CharField(choices=DATE_RANGE_STATUS,default="single",max_length=40)
    leave_type = models.ForeignKey("app.LeaveType", on_delete=models.CASCADE, related_name="leave_types",null=True)
    status =models.CharField(choices=STATUS,default="pending",max_length=40)
    purpose = models.CharField(max_length=60,null=False,blank=False)
    reviewer =models.ForeignKey("app.CustomUser", on_delete=models.CASCADE, related_name="user_reviwer",null=True)
    reviewer_status =models.CharField(choices=REVIWER_STATUS,default="pending",max_length=40)
    remarks =models.CharField(max_length=60,null=True,blank=True)

    def __str__(self):
        return  f"{self.user.name}:Status :{self.status}"
    
    
class LeavesDates(BaseModel):
    leave =models.ForeignKey("app.Leaves", on_delete=models.CASCADE, related_name="leave_dates",null=True)
    date =models.DateField(null=False,blank=False)
    def __str__(self):
        return f"{self.date}"
    
 