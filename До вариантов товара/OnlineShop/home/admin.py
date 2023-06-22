from django.contrib import admin

# Register your models here.
from .models import *

class SettingAdmin(admin.ModelAdmin):
    list_display = ['title','company','update_at','status']

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name','subject','update_at','status','note']
    list_filter = ['status']
    readonly_fields = ['name','subject','update_at','ip','email','message']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

admin.site.register(Setting,SettingAdmin)
admin.site.register(ContactMessage,ContactMessageAdmin)