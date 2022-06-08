from django.contrib import admin
from apps.user.models import User,Address,UserProfile,Hobbies
# Register your models here.

class UserAdminModel(admin.ModelAdmin):
    list_display = ['id','email','password']

class UserAddressAdminModel(admin.ModelAdmin):
    list_display = ['id','city','state','zipcode','country']

class UserProfileAdminModel(admin.ModelAdmin):
    list_display = ['id','phone','image']

class UserHobbiesAdminModel(admin.ModelAdmin):
    list_display = ['id','name']



admin.site.register(User,UserAdminModel)
admin.site.register(Address,UserAddressAdminModel)
admin.site.register(UserProfile,UserProfileAdminModel)
admin.site.register(Hobbies,UserHobbiesAdminModel)



