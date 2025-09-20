from django.contrib import admin
from app.models.developer_model import Developer
from app.models.device_model import UserDevices, UserLocation
from app.models.holiday_model import HolidayMonthsDates, Holidays
from app.models.leaves_model import LeaveType, Leaves, LeavesDates
from app.models.role_model import Access, AccessItems, Actions, Designation, Roles
from app.models.user_model import CustomUser
from app.models.usermail_model import CompanyUserMails
 
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id","name", "email","mobile", "role","designation"]
    search_fields = ["name","email"]
    list_filter = ["designation"]
    def role(self, obj):
        return ", ".join([d.name for d in obj.role.all()])  
    role.short_description = "role"
    
@admin.register(UserDevices)
class UserDevicesAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "device_name","finger_print"]
 
@admin.register(UserLocation)
class UserLocationAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "latitude","longitude"]
    
admin.site.register(Access)
admin.site.register(AccessItems)
admin.site.register(Actions)
admin.site.register(Roles)
 
@admin.register(CompanyUserMails)
class CompanyUserMailsAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "roles", "designation"]
    def roles(self, obj):
        return ", ".join([d.name for d in obj.role.all()])
    
    roles.short_description = "roles"


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "users"]
    search_fields = ["name"]
    def users(self, obj):
        return ", ".join([user.name for user in obj.designations.all()])
    users.short_description = "Users"
@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "is_super"]
    
admin.site.register(Holidays)
 
@admin.register(HolidayMonthsDates)
class HolidayMonthsDatesAdmin(admin.ModelAdmin):
    list_display = ["id", "year", "date", "month", "purpose"]


# Leave Part
admin.site.register(LeaveType)
 
@admin.register(Leaves)
class LeavesAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status","purpose","reviewer", "reviewer_status", "purpose","leave_type","date_range"]
    search_fields = ["user","reviewer","status"]
    list_filter = ["status","reviewer_status","leave_type"]
    
admin.site.register(LeavesDates)


