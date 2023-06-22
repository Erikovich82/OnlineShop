from django.contrib import admin

from .models import *

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','user_name','address','phone',
                    'city','country','image_tag']




class FAQAdmin(admin.ModelAdmin):
    list_display = ['ordernumber','question','answer','status']
    list_filter = ['status']

admin.site.register(FAQ, FAQAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
