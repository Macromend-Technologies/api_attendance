from django.db import models
from django.utils import timezone
from app.models.base_model import BaseModel
from app.models.user_model import CustomUser

class Attendance(BaseModel):
    MARK_CHOICES = (
        ("IN", "Check In"),
        ("OUT", "Check Out"),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="attendances")
    mark_type = models.CharField(max_length=3, choices=MARK_CHOICES)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    time = models.DurationField(null=True, blank=True)
    image = models.ImageField(upload_to="attendance_images/", null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    fingerprint = models.CharField(max_length=100, null=True, blank=True)
  
    def __str__(self):
        return f"{self.user.name} - {self.mark_type} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
