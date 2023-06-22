from django.contrib import admin
from django.urls import path

from . import views
urlpatterns = [
    path('', views.index, name='order_index'),
    path('addtoshopcart/<int:id>', views.addtoshopcart, name='addtoshopcart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
    path('orderproduct/', views.orderproduct, name='orderproduct'),
    # path('<int:id>/<slug:slug>', views.product_detail, name='product_detail'),


]
