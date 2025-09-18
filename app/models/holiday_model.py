from app.models.base_model import BaseModel
from django.db import models
import datetime

class Holidays(BaseModel):
    year = models.IntegerField(unique=True, default=datetime.date.today().year)
   
    
    def __str__(self):
        return  str(self.year)
    
    
class HolidayMonthsDates(BaseModel):
    year = models.ForeignKey("app.Holidays", on_delete=models.CASCADE, related_name="holidays_year",null=True)
    month =models.CharField(max_length=20,null=False)
    date =models.IntegerField(null=False,blank=False)
    purpose = models.CharField(max_length=80,null=False,blank=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['year', 'month', 'date'], 
                name='unique_holiday_per_day'
            )
        ]

    def __str__(self):
  
        return f"{self.date}/{self.month}/{self.year.year}"
      