from django.contrib import admin
from django.urls import path

from . import views
urlpatterns = [
    path('', views.index),
    path('login/',views.login_form, name='login'),
    path('register/',views.register, name='register'),
    path('myaccount/',views.myaccount, name='myaccount'),
    path('wishlist/',views.wishlist, name='wishlist'),
    path('logout/', views.logout_func, name='logout'),
    path('update/', views.user_update, name='user_update'),
    path('orders/', views.user_orders, name='user_orders'),
    path('orderdetail/<int:id>',views.user_orderdetail, name='user_orderdetail'),
    path('order_product/', views.user_order_product, name='user_order_product'),
    path('comments/', views.user_comments, name='user_comments'),
    path('password/', views.password_update, name='password_update'),
]
