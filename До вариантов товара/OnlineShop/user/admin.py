from django.contrib import admin

from .models import *

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','user_name','address','phone',
                    'city','country','image_tag']

admin.site.register(UserProfile, UserProfileAdmin)
