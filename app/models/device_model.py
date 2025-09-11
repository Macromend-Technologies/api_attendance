
from app.models.base_model import BaseModel
from django.db import models
from app.models.user_model import CustomUser

class UserDevices(BaseModel):
    user = models.ForeignKey("app.CustomUser", on_delete=models.CASCADE, related_name="user_device",null=True)
    device_name = models.CharField(max_length=15,null=True,blank=True)
    finger_print = models.CharField(max_length=200,null=True,blank=True)
    
    def __str__(self):
        return  f"{self.user.name}--{self.device_name}"
    
    
class UserLocation(BaseModel):
    user = models.ForeignKey("app.CustomUser", on_delete=models.CASCADE, related_name="user_location",null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=6,blank=True, null=True,)
    longitude= models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True,)
    def __str__(self):
        return  f"{self.user.name}--{self.latitude} -- {self.longitude}"
    
    
      