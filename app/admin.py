from django.contrib import admin

from app.models.device_model import UserDevices, UserLocation
from app.models.user_model import CustomUser
 

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(UserDevices)
admin.site.register(UserLocation)


