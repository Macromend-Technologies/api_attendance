from django.contrib import admin

from app.models.developer_model import Developer
from app.models.device_model import UserDevices, UserLocation
from app.models.role_model import AccessTypes, Roles
from app.models.user_model import CustomUser
from app.models.usermail_model import CompanyUserMails
 

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(UserDevices)
admin.site.register(UserLocation)
admin.site.register(Roles)
admin.site.register(AccessTypes)
admin.site.register(CompanyUserMails)
admin.site.register(Developer)




