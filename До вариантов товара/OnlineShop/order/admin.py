from django.contrib import admin
from .models import *


# Register your models here.

class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'user', 'price', 'amount']
    list_filter = ['user']


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user','product','price','quantity','amount')
    can_delete = False
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name',
                    'last_name',
                    'phone',
                    'city',
                    'total',
                    'status']
    list_filter = ['status']
    readonly_fields = ( 'code',
                        'user',
                       'address',
                       'country',
                       'ip',
                       'first_name',
                       'last_name',
                       'phone',
                       'city',
                       'total')
    can_delete = False

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'product',
                    'price',
                    'quantity',
                    'amount',
                    ]
    list_filter = ['status']

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(ShopCart, ShopCartAdmin)